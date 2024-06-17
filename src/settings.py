
MODEL_LLM = "mistral"

EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"

DATA_PATH = "data"
UPLOADS_PATH = "data/uploads/"
CHROMA_PATH = "data/chroma"
SQLITE_PATH = "data/sqlite/"


DATABASE_NAME = "database.db"

SQL_REQUEST = """
    SELECT llm.name, llm.tokens
    FROM Large_Langage_Model llm
"""


