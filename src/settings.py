
MODEL_LLM = "mistral"

EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"

DATA_PATH = "data"
UPLOADS_PATH = "data/uploads/"
CHROMA_PATH = "data/chroma"
SQLITE_PATH = "data/sqlite/"


DATABASE_NAME = "database.db"

SQL_REQUEST = """
    SELECT t1.id, t1.value, t2.description 
    FROM table1 t1 
    JOIN table2 t2 ON t1.id = t2.id
"""


