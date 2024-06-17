

class AnswerFormat(Exception):
    def __init__(self):
        self.message = "The llm failed to give a json format answer."
        super().__init__(self.message)  