from collections import Counter

from src.utils.int_analyzer import IntAnalyzer

class TupleAnalyzer:
    """
        A class to analyze and process tuples.

        Methods
        -------
        get_lengths(tuples) -> set
            Returns a set of the lengths of the tuples provided.
            
        get_most_frequent_tuples(responses, threshold) -> list
            Returns a list of tuples that appear at least `threshold` times in the responses.
            
        treat_results(results: str) -> list
            Processes a string representation of tuples, converting and cleaning their elements,
            and returns a list of tuples with the processed elements.
    """

    def __init__(self) -> None:
        self.int_analyzer = IntAnalyzer()

    def get_lengths(self, tuples):
        return set([len(t) for t in tuples])


    def get_most_frequent_tuples(self, responses, threshold):
        tuple_counts = Counter(responses)
        frequent_tuples = [t for t, count in tuple_counts.items() if count >= threshold]
        return frequent_tuples

    def treat_results(self, results: str) -> list:
        final_list = []
        results = results.split("), (")
        for element in results:
            liste = element.replace("(", "").replace(")", "")
            liste = liste.replace("]", "").replace("[", "")
            liste = liste.replace("'", "")
            
            liste = liste.split(",")
            liste_analyzed = []
            for data in liste:
                data = data.lstrip()
                data = data.lower()
                data = self.int_analyzer.convert_suffix_to_number(data)
                data = self.int_analyzer.replace_units(data)
                data = self.int_analyzer.try_cast_as_integer(data)
                liste_analyzed.append(data)
            final_list.append(tuple(liste_analyzed))
        return final_list