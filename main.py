"""
    To run it locally,

    streamlit run main.py
"""

# from chat import Chat
from src.sql.database import Database
from src.prompt import PromptManage
from src.llm import Llm
from src.utils.string import StringGenerator
from src.sql.sqlHandler import SqlHandler
from src.settings import *


class Main:
    def __init__(self):
        # self.interface = Chat()
        # self.interface.window()

        # SQL
        self.sql_handler = SqlHandler(SQL_REQUEST)
        self.tables = self.sql_handler.extract_relation_schemes()

        # Database
        self.database = Database(DATABASE_NAME)

        # llm
        self.llm = Llm()
        self.prompt_manager = PromptManage()
        self.sql_answer = []

        # utils
        self.string_generator = StringGenerator()
    

    def run(self):
        # training
        self.llm.get_chat_chain(UPLOADS_PATH + "paper.md")

        # llm
        self.prompt = self.prompt_manager.extract_data_from_text(self.tables)
        self.answer = self.llm.ask(self.prompt)

        # json
        self.bdd_dict = self.string_generator.extract_llm_answer_dict(self.answer)
        print(self.bdd_dict)

        # sql
        self.database.create_tables(self.tables)
        self.database.fill_tables(self.bdd_dict)
        self.sql_answer = self.database.query(SQL_REQUEST, [])
        print(self.sql_answer)




if __name__ == "__main__":
    main = Main()
    main.run()