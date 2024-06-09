
import sqlite3
from src.settings import *
class Database:
    def __init__(self, name):
        self.conn = None
        self.cursor = None

        self.name = name
        self.connect(name)

    def connect(self, db):
        self.conn = sqlite3.connect(SQLITE_PATH + db)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def query(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    def create_table(self, table_name, columns):
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.cursor.execute(f"CREATE TABLE {table_name} ({', '.join(columns)})")
        self.conn.commit()
    
    def create_tables(self, tables_dict):
        for table_name, columns in tables_dict.items():
            self.create_table(table_name, columns)
        
    def fill_table(self, table_name, columns, values):
        self.cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?']*len(columns))})", values)
        self.conn.commit()

    def fill_tables(self, json_answer):
        for table_name, table in json_answer.items():
            columns = table["column_names"]
            data = table["data"]
            for row in data:
                values = [f"'{value}'" if isinstance(value, str) else str(value) for value in row.values()]
                self.fill_table(table_name, columns, values)


    

    