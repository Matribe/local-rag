

from src.utils.int_analyzer import IntAnalyzer

class DatabaseTableAnalyzer:
    """
        A class to analyze database tables and their attributes.

        Methods
        -------
        tables_bulletpoints(tables_dict) -> str
            Generates a formatted string with table names and their columns in bullet points.
            
        type_of_attributs(tables, answer) -> dict
            Determines the types of attributes for each column in the tables, assuming all columns are TEXT by default and converting to INTEGER where applicable.
    """

    def __init__(self) -> None:
        self.int_analyzer = IntAnalyzer()

    def tables_bulletpoints(self, tables_dict) -> str:
        string = ""
        for table, columns in tables_dict.items():
            string += f"{table} :\n"
            for column in columns:
                string += f" - {column}\n"
        return string


    def type_of_attributs(self, tables, answer):
        table_with_type = {}
        for table, columns in tables.items():
            table_with_type[table] = {"column_names": columns}
            table_with_type[table]["type"] = ["TEXT" for _ in columns]
            if answer[table]["data"]:
                attributs = answer[table]["data"][0]
                for i in range(len(columns)):
                    attribut = attributs[i]
                    if self.int_analyzer.is_integer(attribut):
                        table_with_type[table]["type"][i] = "INTEGER"
        return table_with_type
    

