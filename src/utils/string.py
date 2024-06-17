

import json


class StringGenerator:
    def __init__(self):
        pass

    def tables_bulletpoints(self, tables_dict):
        string = ""
        for table, columns in tables_dict.items():
            string += f"{table} :\n"
            for column in columns:
                string += f" - {column}\n"
        return string
    
    def extract_llm_answer_dict(self, answer):
        answer = answer.replace("'", '"')
        return json.loads(answer)
    
    

