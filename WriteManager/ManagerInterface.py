from DataWriter.WriterInterface import Writer


class Manager:
    def __init__(self):
        self.writers = {}

    def add_writer(self, writer: Writer):
        self.writers[writer.table] = writer

    def manage(self):
        raise NotImplementedError
