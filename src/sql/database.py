
import sqlite3
from src.settings import *
import os
class Database:
    def __init__(self, name):
        self.conn = None
        self.cursor = None

        self.name = name
        self.connect(name)

    def connect(self, db):
        db_path = os.path.join(SQLITE_PATH, db)
        db_dir = os.path.dirname(db_path)

        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        if not os.path.exists(db_path):
            with open(db_path, 'w') as f:
                pass

        self.conn = sqlite3.connect(SQLITE_PATH + db)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()


    def execute(self, query, params=None):
        if not params:
            self.cursor.execute(query)
            self.conn.commit()
        else:
            self.cursor.execute(query, params)
            self.conn.commit()


    def create_table(self, table_name, columns):
        self.execute(f"DROP TABLE IF EXISTS {table_name}")
        columns_sql = ", ".join([f"{col} TEXT" for col in columns])
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
        self.execute(create_table_sql)

        
        
    def insert_data(self, table_name, columns, data):
        placeholders = ", ".join(["?" for _ in columns])
        insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        self.execute(insert_sql, [str(data.get(col, '')) for col in columns])


    def process_json(self, json_data, parent_table_name=None):
        for table_name, records in json_data.items():
            if isinstance(records, list):
                columns = set()
                for record in records:
                    columns.update(record.keys())
                columns = list(columns)
                self.create_table(table_name, columns)
                for record in records:
                    self.insert_data(table_name, columns, record)
            elif isinstance(records, dict):
                self.process_json(records, table_name)


    

    