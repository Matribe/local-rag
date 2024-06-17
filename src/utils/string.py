
from src.exceptions import llmException
import json


class StringGenerator:
    def __init__(self):
        pass

    def tables_bulletpoints(self, tables_dict):
        string = ""
        for table, columns in tables_dict.items():
            string += f"Table {table} :\n"
            for column in columns:
                string += f" - {column}\n"
        return string
    
    def extract_llm_answer_dict(self, answer):
        json_part = answer.split("```json")[1].split("```")[0]
        if json_part == "":
            raise llmException
        return json.loads(json_part)
    




    

