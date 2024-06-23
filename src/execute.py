from src.sql.database import Database
from src.prompt import PromptManage
from src.llm import Llm
from src.utils.database_table_analyzer import DatabaseTableAnalyzer
from src.utils.tuple_analyzer import TupleAnalyzer
from src.utils.tuple_manage import TupleManage
from src.sql.sqlHandler import SqlHandler
from src.settings import *

class Execute:

    def __init__(self, query: str) -> None:

        # SQL
        self.sql_handler = SqlHandler(query)
        self.tables = self.sql_handler.extract_relation_schemes()

        # Database
        self.database = Database(DATABASE_NAME)

        # llm
        self.llm = Llm()
        self.prompt_manager = PromptManage()
        self.sql_answer = []

        # utils
        self.tuple_analyzer = TupleAnalyzer()
        self.tuple_manage = TupleManage()
        self.database_table_analyzer = DatabaseTableAnalyzer()

        
