import pandas as pd
import duckdb 

from sqlParser import SqlParser

from exceptions.sqlExceptions import *

class SqlSynthaxValidator():

    def __init__(self, query):
        self.query = query
        self.parser = SqlParser(query)

# Check all the conditions and raise specific error

    def is_query_valid(self) -> bool:

        if self.are_relation_schemes_extractable() == False:
            raise QueryNotValid
        
        if self.are_relation_schemes_empty() == True:
            raise EmptyQueryError

        return True


# Check if the parser can be use

    def are_relation_schemes_extractable(self) -> bool:
       
        attributes_extractable_result = self.are_attributes_extractable()
        tables_extractable_result = self.are_tables_extractables()
        
        final_result = attributes_extractable_result and tables_extractable_result
        
        return final_result

    def are_attributes_extractable(self) -> bool:
        
        try:
            self.parser.find_attributes()
        
        except:
            return False
        
        return True

    def are_tables_extractables(self) -> bool:
        
        try:
            self.parser.find_tables()
        
        except:
            return False
        
        return True


# Check if the results aren't empty

    def are_relation_schemes_empty(self) -> bool:

        attributes__result = self.are_attributes_empty()
        tables_result = self.are_tables_empty()

        final_result = attributes__result and tables_result

        return final_result

    def are_attributes_empty(self) -> bool:
        
        attributes: list[str] = self.parser.find_attributes()

        if attributes:
            return False

        return True

    def are_tables_empty(self) -> bool:

        tables  = self.parser.find_tables()

        if tables:
            return False
        
        return True


# Check the query intern structure with duckdb explain

    def is_query_executable(self, relation_schemes: dict) -> bool:

        db = duckdb.connect()

        for table in relation_schemes:
            
            attributes: list[str] = relation_schemes[table]

            db.register(table, pd.DataFrame(columns=attributes))

        try:
            db.execute(f"EXPLAIN {self.query}")
            return True
        
        except:
             raise QueryNotExecutable   
