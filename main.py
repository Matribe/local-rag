# from chat import Chat
from src.prompt import PromptManage
from src.llm import Llm
from src.utils.string import StringGenerator


class Main:
    def __init__(self):
        # self.interface = Chat()
        # self.interface.window()

        # TODO --------->  get tables from request

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
        self.llm.get_chat_chain("data/uploads/paper.md")

        # llm
        self.prompt = self.prompt_manager.extract_data_from_text(self.tables)
        self.answer = self.llm.ask(self.prompt)

        # json
        self.bdd_dict = self.string_generator.extract_llm_answer_dict(self.answer)
        print(self.bdd_dict)

        # sql
        # TODO --------->  database creation
        # TODO --------->  sql request execution




if __name__ == "__main__":
    main = Main()
    main.run()