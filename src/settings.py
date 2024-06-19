
MODEL_LLM = "mistral"

EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"

DATA_PATH = "data"
UPLOADS_PATH = "data/uploads/"
CHROMA_PATH = "data/chroma"
SQLITE_PATH = "data/sqlite/"


DATABASE_NAME = "database.db"

SQL_REQUEST = """
SELECT r.model_name 
FROM Overview_of_LLM r JOIN 
Large_Language_Models o
ON r.model_name = o.model_name;
"""

NUMBER_OF_GENERATIONS = 20

INITIAL_INDEX_TUPLE = 0