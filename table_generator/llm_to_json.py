import json


class LlmToJson:
    def __init__(self):
        pass

    def convert_to_json(self, answer):
        json_part = answer.split("```json")[1].split("```")[0]
        return json.loads(json_part)
    


        