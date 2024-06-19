from src.sql.database import Database
from src.prompt import PromptManage
from src.llm import Llm
from src.utils.string import StringAnalyze
from src.sql.sqlHandler import SqlHandler
from src.settings import *



class Main:
    def __init__(self):
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
        self.string_analyze = StringAnalyze()
    

    def run(self):
        # Embeddings
        self.llm.get_chat_chain(UPLOADS_PATH + "paper.md")
        self.llm.get_chat_chain(UPLOADS_PATH + "ESCALADE_ReglementUNSS.docx")
        self.llm.get_chat_chain(UPLOADS_PATH + "Lost in the middle.pdf")
        self.llm.get_chat_chain(UPLOADS_PATH + "QueryingLLMwithSQL.pdf")
        print("\n------- La requête : -------")
        print(SQL_REQUEST)


        # Llm
        self.answer = {}
        for table, columns in self.tables.items():
            self.answer[table] = {"column_names": columns}
            data_cache = []
            for _ in range(NUMBER_OF_GENERATIONS):
                table_name = str(table).replace("_", " ")

                answer,_ = self.llm.ask(f"{tuple(columns)} for {table_name}", f"Give me some for {tuple(columns)}")

                answer = self.string_analyze.treat_results(answer)
                # answer = self.string_analyze.verif_size_columns(len(columns), answer)
                data_cache.extend(answer)

                print(answer)


            data_cache = self.string_analyze.get_most_frequent_tuples(data_cache, 3)
            

            print(data_cache)

            self.answer[table]["data"] = data_cache 

        
        print("\n------- Réponse du Llm -------")
        print(self.answer)

        self.table_with_type = self.string_analyze.type_of_attributs(self.tables, self.answer)

        # Sql
        self.database.create_tables(self.table_with_type)
        self.database.fill_tables(self.answer)
        self.sql_answer = self.database.query(SQL_REQUEST, [])
        print("\n------- Réponse de la base de donnée -------")
        print(self.sql_answer)


if __name__ == "__main__":
    main = Main()
    main.run()