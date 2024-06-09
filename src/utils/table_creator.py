import sqlite3

class TableCreator:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.cursor.execute(f"CREATE TABLE {table_name} ({', '.join(columns)})")
        self.conn.commit()

    def create_tables(self, tables_dict):
        for table_name, columns in tables_dict.items():
            self.create_table(table_name, columns)
    
    def add_data(self, table_name, data):
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(data)})")
        self.conn.commit()

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

    
    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

        


    