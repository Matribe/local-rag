from src.sql.sqlSynthaxValidator import SqlSynthaxValidator
from src.sql.sqlParser import SqlParser
from src.sql.sqlAliasHandler import SqlAliasHandler

class SqlHandler():

    def __init__(self, query: str):

        self.query: str = query

        self.parser = SqlParser(query)
        self.validator = SqlSynthaxValidator(query)
        self.alias_handler = SqlAliasHandler(query)

        # raise catchable exception if query not valid
        self.validator.is_query_valid()

        # extract for the test
        self.relation_schemes: dict = self.extract_relation_schemes()

        # raise catchable exception if query not executable
        self.validator.is_query_executable(self.relation_schemes)

    def extract_relation_schemes(self) -> dict:
        
        tables: list[str] = self.parser.find_tables()

        relation_schemes = {}

        if len(tables) == 1 :

            attributes = self.parser.find_attributes()

            table = tables[0]
            relation_schemes[table] = attributes

            return relation_schemes

        for table in tables:

            attributes: list[str] = self.extract_attributes_for_specific_table(table)
            relation_schemes[table] = attributes
        
        return relation_schemes

    def extract_attributes_for_specific_table(self, table_name) -> list[str]:
        
        attributes_of_specified_table = []
        all_attributes = self.parser.find_attributes()

        for attribute in all_attributes:

            if table_name in attribute: 
                attribute_without_alias = self.alias_handler.extract_attribute_from_alias(attribute)
                attributes_of_specified_table.append(attribute_without_alias)

        return attributes_of_specified_table

