from DataWriter.WriterInterface import Writer


class Manager:
    name: str

    def __init__(self):
        self.writers = {}

    def add_writer(self, writer: Writer):
        self.writers[writer.table] = writer

    def manage(self, action, data):
        raise NotImplementedError
