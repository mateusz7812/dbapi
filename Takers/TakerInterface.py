from Requests.RequestGeneratorInterface import RequestGenerator
from Forwarders.ForwarderInterface import Forwarder


class Taker:
    def __init__(self, request_generator, forwarder):
        if not issubclass(request_generator, RequestGenerator):
            raise Exception(request_generator + " is not subclass of RequestGenerator")
        if not issubclass(forwarder.__class__, Forwarder):
            raise Exception(forwarder + " is not subclass of Forwarder")
        self.forwarder = forwarder
        self.requestGenerator = request_generator()

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def take(self, data):
        request = self.requestGenerator.generate(data)
        return self.forwarder.forward(request)
