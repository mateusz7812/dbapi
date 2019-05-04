from Writers.WriterInterface import Writer


class Manager:
    name: str

    def __init__(self):
        self.writers = {}

    def add_writer(self, writer):
        #if not issubclass(writer.__class__, Writer):
        #    raise Exception(writer + " is not subclass of Writer")
        self.writers[writer.table] = writer

    def manage(self, action, data):
        raise NotImplementedError
