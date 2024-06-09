'''
    Externals importations.
'''
import pandas as pd
import duckdb
'''
    Internals importations.
'''
from src.relationScheme import RelationScheme
from src.aliasHandler import AliasHandler

class DbHandler:
    '''
        TOOL:
            This class is a handler for generating attribute tables and explaining SQL queries using DuckDB.
    '''
    def generate_attributes_table(self, relation_scheme:RelationScheme) -> pd.DataFrame:
        '''
            Creates a DataFrame based on the attributes of a given relation scheme.
        '''
        temporary_dict = {}
        for attribute in relation_scheme.attributes:
            temporary_dict[attribute] = []
        return pd.DataFrame(temporary_dict)
    
    def explain_with_duckdb(self, sql_formula:str, relation_schemes:list[RelationScheme]) -> str:
        '''
            This method connects to DuckDB, registers each relation scheme as a table, 
            executes an EXPLAIN query on the given SQL formula, and returns the query plan as a string.
        '''
        db = duckdb.connect()
        for relation_scheme in relation_schemes:
            if(AliasHandler().has_alias(relation_scheme.name)):
                db.register(AliasHandler().strip_alias_from_table(relation_scheme.name), self.generate_attributes_table(relation_scheme))
            else:
                db.register(relation_scheme.name, self.generate_attributes_table(relation_scheme))
        result = db.execute("EXPLAIN "+sql_formula).fetchall()
        result = list(result[0])
        result.pop(0)
        result = "".join(result)
        return result

    