class DataWorker:
    def prepare(self):
        raise NotImplementedError

    def insert(self, values: {}):
        raise NotImplementedError

    def select(self, values: {}):
        raise NotImplementedError

    def delete(self, values: {}):
        raise NotImplementedError

    def update(self, values: {}):
        raise NotImplementedError
