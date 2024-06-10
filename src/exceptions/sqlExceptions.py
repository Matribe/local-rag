class QueryNotValid(Exception):

    def __init__(self) -> None:
        self.message = "The specified query isn't in a valid form."
        super().__init__(self.message)

class QueryNotExecutable(Exception):

    def __init__(self) -> None:
        self.message = "The specified query isn't executable."
        super().__init__(self.message)

class EmptyQueryError(Exception):

    def __init__(self) -> None:
        self.message = "The specified query is empty."
        super().__init__(self.message)