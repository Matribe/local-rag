
import sqlite3

class Sql:
    def __init__(self, db_name):
        self.conn = None
        self.cursor = None

        self.db_name = db_name
        self.connect(db_name)

    def connect(self, db):
        self.conn = sqlite3.connect(db)
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


    

    