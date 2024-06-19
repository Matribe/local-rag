
MODEL_LLM = "mistral"

EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"

DATA_PATH = "data"
UPLOADS_PATH = "data/uploads/"
CHROMA_PATH = "data/chroma"
SQLITE_PATH = "data/sqlite/"


DATABASE_NAME = "database.db"

SQL_REQUEST = """
SELECT llm.model, llm.number_of_parameters
FROM Large_Langage_Model llm
"""

NUMBER_OF_GENERATIONS = 20

INITIAL_INDEX_TUPLE = 0