from src.sql.sqlParser import SqlParser
from src.exceptions.aliasExceptions import AttributeWithoutAlias

class SqlAliasHandler():

    def __init__(self, query: str) -> None:
        
        self.query = query
        
        self.parser = SqlParser(query)

        self.attributes = self.parser.find_attributes()
        self.tables = self.parser.find_tables()


# Check if the query is correctly aliased

    def is_query_aliased(self) -> bool:
        
        all_tables_aliased_result = self.are_all_tables_aliased()
        all_attributes_aliased_result = self.are_all_attributes_aliased()

        final_result = all_tables_aliased_result and all_attributes_aliased_result

        return final_result


# Check tables aliases

    def are_all_tables_aliased(self) -> bool:
        
        all_tables_AS_aliased_result = self.are_all_tables_AS_aliased()
        all_tables_space_aliased_result = self.are_all_tables_space_aliased()

        final_result = all_tables_AS_aliased_result or all_tables_space_aliased_result

        return final_result

    def are_all_tables_AS_aliased(self) -> bool:
        
        tables = self.tables
        query_as_list = self.query.split(' ')
        len_query_list = len(query_as_list)

        for table in tables:
            
            index_table_in_query = query_as_list.index(table)

            if index_table_in_query+1>len_query_list:
                return False
            
            elif query_as_list[index_table_in_query+1] != 'AS':
                return False 
            
        return True

    def are_all_tables_space_aliased(self) -> bool:
        tables = self.tables
        query_as_list = self.query.split(' ')
        len_query_list = len(query_as_list)

        for table in tables:
            
            index_table_in_query = query_as_list.index(table)

            if index_table_in_query+1>len_query_list:
                return False
            
            elif query_as_list[index_table_in_query+1] == 'JOIN':
                return False

            elif query_as_list[index_table_in_query+1] == ',':
                return False
            
        return True


# Check attributes aliases

    def are_all_attributes_aliased(self) -> bool:
        
        attributes = self.attributes
        
        for attribute in attributes:
            
            if self.is_attribute_aliased(attribute) == False:
                return False
            
        return True

    def is_attribute_aliased(self, attribute) -> bool:
        alias,_,attribute_name = attribute.partition(".")

        if not attribute_name or alias == attribute:
            return False
        
        return True


# Extract attributes from aliases

    def extract_attribute_from_alias(self, attribute: str) -> str:
        
        if self.is_attribute_aliased(attribute) == False:
            raise AttributeWithoutAlias

        _,_,attribute_without_alias = attribute.partition(".")

        return attribute_without_alias

    def extract_attributes_from_aliases(self, attributes: list[str]) -> list[str]:

        if self.are_all_attributes_aliased() == False:
            raise AttributeWithoutAlias
        
        attributes_without_aliases = []

        for attribute in attributes:
            
            attribute_without_alias = self.extract_attribute_from_alias(attribute)
            attributes_without_aliases.append(attribute_without_alias)
        
        return attributes_without_aliases