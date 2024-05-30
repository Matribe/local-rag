class MultiTablesInQueryWithoutAlias(Exception):

    def __init__(self):
        self.message = "There are multi tables in the query but at least one of them has no alias,\nit's impossible to clearly define the attributes of each tables"
