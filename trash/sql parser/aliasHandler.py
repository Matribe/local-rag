'''
    Internals importations.
'''
from src.sqlParser import SqlParser
from src.randomSequenceGenerator import RandomSequenceGenerator
'''
    Internal Exception management importations.
'''
from exceptions.aliasExceptions import NameWithNoAlias
from exceptions.aliasExceptions import MultipleFormatAlias


class AliasHandler:
    """
        TOOL:
            AliasHandler is a utility class that provides methods for handling SQL table and attribute aliases. 
            This class includes functions to:
            - Verify the usage of "AS" format aliases in SQL formulas.
            - Convert "AS" format aliases to dot format aliases.
            - Extract tables and attributes in dot alias format.
            - Check if all elements (tables or attributes) have aliases.
            - Retrieve and strip aliases from table and attribute names.
            - Verify if a name contains an alias.
            These methods facilitate the manipulation and validation of SQL queries, ensuring proper alias formatting and extraction.
    """
    def is_AS_format_alias_used(self, tables:list[str], sql_formula:str) -> bool:
        '''
            Checks if the tables in the SQL formula use the "AS" alias format. 
        '''
        tag = RandomSequenceGenerator().generate()
        for table in tables:
            sql_formula = sql_formula.replace(table, tag)
        sql_formula_split = sql_formula.split() 
        for index, element in enumerate(sql_formula_split):
            if element == tag and index < len(sql_formula_split) - 1:
                if sql_formula_split[index + 1] != "AS":
                    return False
            if element == tag and index >= len(sql_formula_split) - 1:
                return False
        return True
        
    def convert_to_dot_alias_format(self, tables:list[str], sql_formula:str) -> str:
        '''
            Converts the "AS" alias format in the SQL formula to the dot alias format. 
        '''
        if not (self.is_AS_format_alias_used(tables, sql_formula)):
            raise MultipleFormatAlias
        formated_sql_formula = []
        alias_list = []
        sql_formula_split = sql_formula.split() 
        for index, element in enumerate(sql_formula_split):
            if element != "AS" and element not in alias_list :
                if element in tables and index < len(sql_formula_split) - 2:
                    formated_sql_formula.append(f"{element}.{sql_formula_split[index+2]}")
                    alias_list.append(sql_formula_split[index+2])
                else:
                    formated_sql_formula.append(element)
        return " ".join(formated_sql_formula)
    
    def extract_dot_alias_tables(self, tables:list[str], sql_formula:str) -> list[str]:
        '''
            Retrieves tables in the SQL formula using the dot alias format
        '''
        if not (self.is_AS_format_alias_used(tables, sql_formula)):
            raise MultipleFormatAlias
        tables_with_alias = []
        alias_list = []
        sql_formula_split = sql_formula.split() 
        for index, element in enumerate(sql_formula_split):
            if element != "AS" and element not in alias_list :
                if element in tables and index < len(sql_formula_split) - 2:
                    tables_with_alias.append(f"{element}.{sql_formula_split[index+2]}")
                    alias_list.append(sql_formula_split[index+2])
        return tables_with_alias
    
    def extract_aliases_from_dot_tables(self, dot_tables:list[str]) -> dict:
        '''
            Extracts aliases from tables using the dot alias format.
        '''
        temp_dict = {}
        for table in dot_tables:
            if not (self.has_alias(table)):
                raise NameWithNoAlias
            temp_dict[table.split(".")[0]] = table.split(".")[1]
        return temp_dict
    
    def convert_attributes_to_dot_alias_format(self, dot_tables:list[str], attributes:list[str]) -> list[str]:
        '''
            Converts attributes to the dot alias format using the given dot tables.
        '''
        alias_dictionnary = self.extract_aliases_from_dot_tables(dot_tables)
        transformed_attributes = []
        for attribute in attributes:
            if not(self.has_alias(attribute)):
                raise NameWithNoAlias
            if(attribute.split(".")[0] in alias_dictionnary):
                transformed_attributes.append(f"{alias_dictionnary[attribute.split('.')[0]]}.{attribute.split('.')[1]}")
        return transformed_attributes
    
    def is_transformable_to_dot_alias(self, tables:list, attributes:list, sql_formula:str):
        '''
            Checks if the SQL formula can be transformed to use dot aliases.
        '''
        if not(self.is_AS_format_alias_used(tables, sql_formula)):
            return False
        sql_formula = self.convert_to_dot_alias_format(tables, sql_formula)
        tables = SqlParser().find_tables(sql_formula)
        if not (self.are_aliases_applicable(tables, attributes)):
            return False
        return True

    def apply_aliases_to_sql_formula(self, tables:list[str], sql_formula:str) -> str:
        '''
            Transforms the SQL formula to use "AS" aliases for the given tables. 
        '''
        for table in tables:
            sql_formula = sql_formula.replace(table, f"{self.strip_alias_from_table(table)} AS {self.extract_alias_from_table(table)}")
        return sql_formula

    def are_aliases_applicable(self, tables:list, attributes:list) -> bool:
        ''' 
            Checks if all tables and attributes have aliases.
        '''
        return self.is_all_elements_with_alias(tables) and self.is_all_elements_with_alias(attributes)

    def find_attributes_from_alias(self, table_name:str, sql_formula:str) -> list:
        '''
            Finds attributes associated with a specific table alias in the SQL formula.
        '''
        if not(self.has_alias(table_name)):
            raise NameWithNoAlias
        alias = f"{self.extract_alias_from_table(table_name)}."
        attributes = []
        for attribute in SqlParser().find_attributes(sql_formula):
            if(alias in attribute):
                attributes.append(self.strip_alias_from_attribute(attribute))
        return attributes

    def is_all_elements_with_alias(self, elements:list) -> bool:
        '''
            Checks if all elements in the list have aliases.
        '''
        for element in elements:
            if not(self.has_alias(element)):
                return False
        return True
    
    def has_alias(self, name:str) -> bool:
        '''
            Checks if the given name contains an alias.
        '''
        return len(name.split(".")) == 2
    
    def extract_alias_from_attribute(self, attribute_name:str):
        ''' 
             Retrieves the alias from the given attribute name.
        '''
        return self.extract_name_part(attribute_name, 0)

    def extract_alias_from_table(self, table_name:str):
        '''
            Retrieves the alias from the given table name.
        '''
        return self.extract_name_part(table_name, 1)
    
    def strip_alias_from_attribute(self, attribute_name:str):
        ''' 
            Removes the alias from the given attribute name.
        '''
        return self.extract_name_part(attribute_name,1)
    
    def strip_alias_from_table(self, table_name:str):
        ''' 
            Removes the alias from the given table name.
        '''
        return self.extract_name_part(table_name,0)

    def extract_name_part(self, name:str, place:int) -> str:
        '''
            Extracts a specific part of the name based on the given position.
        '''
        if not (self.has_alias(name)):
            raise NameWithNoAlias
        return name.split(".")[place]
            