from Requests.RequestGeneratorInterface import RequestGenerator


class Taker:
    def __init__(self, request_generator: RequestGenerator, forwarder):
        self.requestGenerator = request_generator
        self.forwarder = forwarder

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def take(self):
        raise NotImplementedError