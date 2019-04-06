from DataWriter.WriterInterface import Writer


class WritersGenerator:
    def __init__(self, writer: Writer):
        self.writer = writer

    def generate_writer(self):
        raise NotImplementedError
