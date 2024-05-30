class NameWithNoAlias(Exception):

    def __init__(self) -> None:
        self.message = "The specified name (table, attribute) has no alias in its composition."

class MultipleFormatAlias(Exception):

    def __init__(self) -> None:
        self.message = "The query is containing multiple formats alias, they need to be in only one format."