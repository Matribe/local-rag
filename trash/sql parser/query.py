'''
    Externals importations.
'''
import pandas as pd
'''
    Internals importations.
'''
from src.relationScheme import RelationScheme
from src.sqlExplainer import SqlExplainer
from src.sqlParser import SqlParser
from src.aliasHandler import AliasHandler
from src.dataHandler import DataHandler
'''
    Internal Exception management importations.
'''
from exceptions.queryExceptions import *

class Query:
    ''' 
        OBJECT:
            This class is an object representing a sql query and extracts all its components.
            The constructor only takes the sql formula as text and it extracts all the attributes,
            tables names and relations schemes. It can build the query plan diagram as text or
            as a dataframe.
    '''
    sql_formula:str
    relation_schemes:RelationScheme
    operators:list
    arguments:list

    def __init__(self, sql_formula:str) -> None:
        '''
            Constructor of a Query object, which represent a sql query with : 
                - sql_formula:str it's the sql formula in text.
                - tables:list it's all the tables names
                - attributes:list it's all the attributes from all the tables in the query
                - relation_schemes:list it's all the relation scheme objects extracted from
                                        the text of the sql formula.
                - operators:list it's the operators in the sql formula.
        '''
        self.sql_formula = sql_formula
        self.tables = self.find_tables()
        self.attributes = self.find_attributes()
        self.relation_schemes = self.find_relations_schemes()
        self.operators = self.find_operators()

    def find_tables(self) -> list[str]:
        '''
            Method returning a list containing all the tables
            names in a sql query.
        '''
        return SqlParser().find_tables(self.sql_formula)
    
    def find_attributes(self) -> list[str]:
        '''
            Method returning a list containing all the attributes
            in a sql query.
        '''
        return SqlParser().find_attributes(self.sql_formula)
    
    def find_operators(self) -> list[str]:
        ''' 
            Method retrurning all the sql operators in a query.
        '''
        operators = []
        for word in self.sql_formula.split(" "):
            if(word.upper() in DataHandler().get_operators_as_list()):
                operators.append(word)
        return operators

    def find_relations_schemes(self) -> list[RelationScheme]:
        '''
            Method returning a list of RelationScheme for all the tables present in the sql query.
            If the format of the sql formula is not recognized, it raises an MultiTablesInQueryWithoutAlias
            exception. 
        '''
        relation_schemes = []
        if(AliasHandler().are_aliases_applicable(self.tables, self.attributes) or AliasHandler().is_transformable_to_dot_alias(self.tables, self.attributes, self.sql_formula)):
            if(AliasHandler().is_transformable_to_dot_alias(self.tables, self.attributes, self.sql_formula)):
                self.process_as_alias()
            for table in self.tables:
                relation_schemes.append(RelationScheme(table,AliasHandler().find_attributes_from_alias(table, self.sql_formula)))
            self.sql_formula = AliasHandler().apply_aliases_to_sql_formula(self.tables, self.sql_formula)
            return relation_schemes
        if not(len(self.tables) == 1):
            raise MultiTablesInQueryWithoutAlias
        return [RelationScheme(self.tables[0], self.attributes)]

    def to_string(self) -> str:
        '''
            Method returning a String representing all the Query's values.
        '''
        relation_schemes_string = ""
        for relation_scheme in self.relation_schemes:
            relation_schemes_string += "\n"+relation_scheme.to_string()+"\n"
        return  f'sql_formula : {self.sql_formula}\nrelation_scheme : \n{relation_schemes_string}\noperators : {self.operators}\nall attributes:{self.attributes}\nall tables:{self.tables}'

    def process_as_alias(self) -> None:
        '''
            Method calling all the handlers for a query using AS aliases. 
        '''
        old_sql_formula = self.sql_formula
        self.sql_formula = AliasHandler().convert_to_dot_alias_format(self.tables, self.sql_formula)
        self.tables = AliasHandler().extract_dot_alias_tables(self.tables, old_sql_formula)
        self.attributes = AliasHandler().convert_attributes_to_dot_alias_format(self.tables, self.attributes)

    def explain(self) -> str:
        '''
            Method calling the sqlExplainer module to produce the query plan diagram.
        '''
        return SqlExplainer().explain(self.sql_formula, self.relation_schemes)
    
    def explain_query_as_dataframe(self) -> pd.DataFrame:
        '''
            Method producing the query plan and returning it as a pandas dataframe. 
        '''
        return SqlExplainer().sql_plan_to_table(self.sql_formula, self.relation_schemes)