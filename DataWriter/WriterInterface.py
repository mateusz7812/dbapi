class Writer:
    def __init__(self, table):
        self.table = table

    def insert(self, values: {}):
        raise NotImplementedError

    def select(self, values: {}):
        raise NotImplementedError

    def delete(self, values: {}):
        raise NotImplementedError
