
import sqlite3
from src.settings import *
import os
class Database:
    '''
        A class to manage SQLite database operations including connection, querying, 
        and table creation.

        Attributes:
            conn (sqlite3.Connection): SQLite database connection object.
            cursor (sqlite3.Cursor): SQLite cursor object for executing SQL commands.
            name (str): Name of the SQLite database file.

        Methods:
            __init__(name):
                Initializes the Database instance and connects to the specified database.

            connect(db):
                Connects to the specified SQLite database file, creating the file and directory if they do not exist.

            close():
                Closes the connection to the SQLite database.

            query(query, params):
                Executes a SELECT query with the provided parameters and returns the fetched results.

            execute(query, params):
                Executes an SQL query with the provided parameters and commits the changes.

            create_table(table_name, columns, types):
                Creates a table with the specified columns and types, dropping any existing table with the same name.

            create_tables(tables_dict):
                Creates multiple tables as defined in the provided dictionary.

            fill_table(table_name, columns, values):
                Inserts a row of data into the specified table.

            fill_tables(json_answer):
                Fills multiple tables with data from a provided dictionary.
    '''
        
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

    def query(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    def create_table(self, table_name, columns, types):
        assert len(columns) == len(types)
        columns_definition = [f"{column} {typ}" for column, typ in zip(columns, types)]
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.cursor.execute(f"CREATE TABLE {table_name} ({', '.join(columns_definition)})")
        self.conn.commit()
    
    def create_tables(self, tables_dict):
        for table_name, columns in tables_dict.items():
            columns_name = columns["column_names"]
            types = columns["type"]
            self.create_table(table_name, columns_name, types)
        
    def fill_table(self, table_name, columns, values):
        self.cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?']*len(columns))})", values)
        self.conn.commit()

    def fill_tables(self, json_answer):
        for table_name, table in json_answer.items():
            columns = table["column_names"]
            data = table["data"]
            for row in data:
                values = [f"'{value}'" if isinstance(value, str) else str(value) for value in row]
                self.fill_table(table_name, columns, values)


    

    