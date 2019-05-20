
class Guard:
    def __init__(self):
        self.authorization_methods = []
        self.processors = {}

    def resolve(self, response):
        raise NotImplementedError

    def add_processor(self, processor):
        self.processors[processor.name] = processor
