


class IntAnalyzer:
    """
        A utility class for analyzing and manipulating strings that represent integers or contain numeric suffixes.

        Methods:
        --------
        is_integer(string: str) -> bool:
            Determines if the given string can be converted to an integer.

        try_cast_as_integer(string: str) -> int | str:
            Attempts to convert the given string to an integer.

        convert_suffix_to_number(string: str) -> int | str:
            Converts a string with a numeric suffix ('k', 'm', 'b') to its integer representation.

        replace_units(string: str) -> int | str:
            Replaces textual numeric units ('thousand', 'million', 'billion', 'trillion') in the string with their numerical equivalents and evaluates the expression.
    """


    def is_integer(self, string: str) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False
    

    def try_cast_as_integer(self, string: str) -> int | str:
        try: 
            integer = int(string)
            return integer
        except:
            return string
        

    def convert_suffix_to_number(self, string: str) -> int | str:
        data = string
        if not data:
            return ""
        if data[-1] in ['k', 'm', 'b'] and data[:-1].isdigit():
            number = int(data[:-1])
            suffix = data[-1]
            if suffix == 'k':
                return number * 1000
            elif suffix == 'm':
                return number * 1000000
            elif suffix == 'b':
                return number * 1000000000
        return string

    def replace_units(self, string: str) -> int | str:
        if not isinstance(string, int):
            data = string.replace('thousand','*10**3').replace('million','*10**6').replace('billion','*10**9').replace('trillion','*10**12')
            if self.is_integer(data[:-6]):
                return int(eval(data))
        return string