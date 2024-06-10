class AttributeWithoutAlias(Exception):

    def __init__(self) -> None:
        self.message = "The specified attribute isn't containing alias."
        super().__init__(self.message)