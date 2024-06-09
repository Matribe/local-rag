import sqlite3

class TableCreator:

    def json_answer_to_tables_dict(self, json_answer):
        tables_dict = {}
        for table_name, table in json_answer.items():
            columns = table["column_names"]
            tables_dict[table_name] = columns
        return tables_dict
    
    def json_to_database(self, json_answer):
        tables_dict = self.json_answer_to_tables_dict(json_answer)
        self.create_tables(tables_dict)
        for table_name, table in json_answer.items():
            data = table["data"]
            for row in data:
                columns = [f"'{value}'" if isinstance(value, str) else str(value) for value in row.values()]
                print(columns)
                self.add_data(table_name, columns)


        


    