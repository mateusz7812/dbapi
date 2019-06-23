from Writers.WriterInterface import DataWriter


class Manager:
    name: str

    def __init__(self):
        self.writers = {}

    def add_writer(self, writer):
        #if not issubclass(writer.__class__, DataWriter):
        #    raise Exception(writer + " is not subclass of DataWriter")
        if writer.prepare():
            self.writers[writer.table] = writer

    def manage(self, action, data):
        raise NotImplementedError
