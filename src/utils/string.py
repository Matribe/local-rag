

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
            liste = liste.replace("]", "").replace("[", "")
            liste = liste.split(",")
            liste_analyzed = []
            for data in liste:
                data = data.lstrip()
                data = self.convert_suffix_to_number(data)
                data = self.replace_units(data)
                liste_analyzed.append(data)
            final_list.append(tuple(liste_analyzed))
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
    
    def is_integer(self, string: str) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False
    
    def type_of_attributs(self, tables, answer):
        table_with_type = {}
        for table, columns in tables.items():
            table_with_type[table] = {"column_names": columns}
            table_with_type[table]["type"] = ["TEXT" for _ in columns]
            if answer[table]["data"]:
                attributs = answer[table]["data"][0]
                for i in range(len(columns)):
                    attribut = attributs[i]
                    if self.is_integer(attribut):
                        table_with_type[table]["type"][i] = "INTEGER"
        return table_with_type
    
    def convert_suffix_to_number(self, string: str):
        data = string.lower()
        if data[-1] in ['k', 'm', 'b'] and data[:-1].isdigit():
            number = int(data[:-1])
            suffix = data[-1]
            if suffix == 'k':
                return number * 1000
            elif suffix == 'm':
                return number * 1000000
            elif suffix == 'b':
                return number * 1000000000
        else:
            return string

    def replace_units(self, string: str) -> str:
        if not isinstance(string, int):
            string = string.lower()
            return string.replace('thousand','*10**3').replace('million','*10**6').replace('billion','*10**9').replace('trillion','*10**12')
        return string