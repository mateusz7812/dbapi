class RequestGeneratorInterface:
    def __init__(self):
        self.request_type = None

    def generate(self, data: {}):
        raise NotImplementedError

