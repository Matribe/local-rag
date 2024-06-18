

from collections import Counter

class StringAnalyze:
    '''
        A class for generating and processing strings from different types of data structures.

        This class provides methods for converting dictionaries to formatted strings,
        extracting dictionaries from JSON-like strings, processing results into lists of tuples,
        and identifying the most frequent tuples in a list of responses.

        Methods
        -------
        tables_bulletpoints(tables_dict: dict) -> str:
            Converts a dictionary of tables and their columns into a formatted string with bullet points.
            
        extract_llm_answer_dict(answer: str) -> dict:
            Converts a JSON-like string answer into a dictionary.

        treat_results(results: str) -> list:
            Processes a string of results into a list of tuples.
            
        get_most_frequent_tuples(responses: list, threshold: int) -> list:
            Identifies and returns the tuples that appear at least `threshold` times in the given list of responses.
    '''


    def tables_bulletpoints(self, tables_dict) -> str:
        string = ""
        for table, columns in tables_dict.items():
            string += f"{table} :\n"
            for column in columns:
                string += f" - {column}\n"
        return string
    
    def treat_results(self, results: str) -> list:
        final_list = []
        results = results.split("), (")
        for element in results:
            liste = element.replace("(", "")
            liste = liste.replace(")", "")
            liste = liste.replace("'", "")
            liste = liste.split(",")
            liste = tuple(liste)
            final_list.append(liste)
        return final_list

    def get_most_frequent_tuples(self, responses, threshold) -> float:
        tuple_counts = Counter(responses)
        frequent_tuples = [t for t, count in tuple_counts.items() if count >= threshold]
        return frequent_tuples
    
    def verif_size_columns(self, size, answer):
        answer_verified = []
        for data in answer:
            if len(data) == size:
                answer_verified.append(data)
        return answer_verified
    
    def is_integer(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False
    
    def type_of_attributs(self, tables, answer):
        if not answer[table]["data"]:
            return []
        table_with_type = {}
        for table, columns in tables.items():
            table_with_type[table] = {"column_names": columns}
            table_with_type[table]["type"] = ["TEXT" for _ in columns]
            attributs = answer[table]["data"][0]
            for i in range(len(columns)):
                attribut = attributs[i]
                if self.is_integer(attribut):
                    table_with_type[table]["type"][i] = "INTEGER"
        return table_with_type