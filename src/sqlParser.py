'''
    Externals importations.
'''
from sql_metadata import Parser as parser

class SqlParser:
    '''
        TOOL:
                This class contains tools for parsing sql queries.
                It can be used to find tables names or attributes in a
                sql query under str format.
    '''
    def find_tables(self,sql_formula:str) -> list:
        '''
            Method using the sql_metadata library to return all the
            tables names in a sql query formula.
        '''
        return (parser(sql_formula).tables)
    
    def find_attributes(self,sql_formula:str) -> list:
        '''
            Method using the sql_metadata library and a completion code
            to return all the attributes in a sql query formula.
        '''
        columns = parser(sql_formula).columns
        if(columns == [] and 'SELECT' in sql_formula):
            sql_formula = sql_formula.split("SELECT ")[1]
            sql_formula = sql_formula.split(" FROM")[0]
            columns.append(sql_formula)
        return (columns)
    
    