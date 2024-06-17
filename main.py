"""
    To run it locally,

    streamlit run main.py
"""

# from chat import Chat
import re

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
        # Embeddings
        self.llm.get_chat_chain(UPLOADS_PATH + "paper.md")
        self.llm.get_chat_chain(UPLOADS_PATH + "ESCALADE_ReglementUNSS.docx")
        self.llm.get_chat_chain(UPLOADS_PATH + "Lost in the middle.pdf")
        self.llm.get_chat_chain(UPLOADS_PATH + "QueryingLLMwithSQL.pdf")
        print("\n------- La requête : -------")
        print(SQL_REQUEST)

        json_final = {}

        for table, columns in self.tables.items():
            json_final[table] = {"column_names": columns}

            for column in columns:
                print(f"\n------- pour {column} de {table} -------")
                # llm
                self.answer, sources = self.llm.ask(f"Give me some {column} of {table}.")
                print("\n------- Réponse du LLM -------")
                print(self.answer)
                print("\n------- Sources utilisées -------")
                print(sources)

                try:
                    resultats = re.search(r'\[(.*?)\]', self.answer).group(1).split(",")
                except:
                    resultats = []

                # try:
                #     resultats = re.search(r'\[(.*?)\]', self.answer).group(1)
                # except:
                #     resultats = ""

                # resultat_final = []
                # for resultat in resultats.split(","):
                #     reponse = self.llm.model.invoke(f"""
                #         <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
                #         to answer the question. If you don't know the answer, just say that you don't know.
                #         [/INST] </s>
                #         <INST>
                #             Answer with Yes or No only. Don't make a sentence, just respond with one word.
                #         </INST>\n
                #         <INST> Question : Is {resultat} a {column} of {table} ?
                #         Context : {sources}
                #         Answer:</INST>""")
                #     if "Yes" in reponse.content:
                #         resultat_final.append(resultat)
                # print("\n------- Résultat final -------")
                # print(resultat_final)

                json_final[table][column] = resultats
        
        print("\n------- le Json obtenu -------")
        print(json_final)



if __name__ == "__main__":
    main = Main()
    main.run()