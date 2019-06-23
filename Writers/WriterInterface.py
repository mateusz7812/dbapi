class DataWriter:
    def prepare(self):
        raise NotImplementedError

    def insert(self, values: {}):
        raise NotImplementedError

    def select(self, values: {}):
        raise NotImplementedError

    def delete(self, values: {}):
        raise NotImplementedError
