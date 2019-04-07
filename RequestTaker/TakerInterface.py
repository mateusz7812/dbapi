from Requests.RequestGeneratorInterface import RequestGenerator


class Taker:
    def __init__(self, request_generator: RequestGenerator):
        self.requestGenerator = request_generator

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def take(self, data):
        raise NotImplementedError
