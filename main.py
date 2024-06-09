# from chat import Chat
from src.prompt import PromptManage
from src.llm import Llm
from src.utils.string import StringGenerator


class Main:
    def __init__(self):
        # self.interface = Chat()
        # self.interface.window()

        self.tables = {
            "table1": ["id", "value"],
            "table2": ["description", "id"]
        }

        # llm
        self.llm = Llm()
        self.prompt_manager = PromptManage()

        # utils
        self.string_generator = StringGenerator()



    def run(self):
        # training
        self.llm.get_chat_chain("uploads/paper.md")

        # llm
        self.prompt = self.prompt_manager.extract_data_from_text(self.tables)
        self.answer = self.llm.ask(self.prompt)

        # json
        self.bdd_dict = StringGenerator.extract_llm_answer_dict(self.answer)

        # sql
        # --------->  database creation
        # --------->  sql request execution




if __name__ == "__main__":
    main = Main()
    main.run()