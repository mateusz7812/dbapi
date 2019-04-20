from Requests.RequestGeneratorInterface import RequestGenerator


class Taker:
    def __init__(self, request_generator, response_generator, forwarder):
        self.forwarder = forwarder
        self.requestGenerator = request_generator
        self.responseGenerator = response_generator

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def take(self, data):
        request = self.requestGenerator.generate(data)
        response = self.responseGenerator.generate(request)
        return self.forwarder.forward(response)
