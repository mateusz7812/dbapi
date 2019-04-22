from Requests.RequestGeneratorInterface import RequestGenerator


class Taker:
    def __init__(self, request_generator, forwarder):
        self.forwarder = forwarder
        self.requestGenerator = request_generator

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def take(self, data):
        request = self.requestGenerator.generate(data)
        return self.forwarder.forward(request)
