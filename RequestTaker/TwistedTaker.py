import json

from twisted.web import resource
from twisted.internet import reactor
from twisted.web import server

from RequestTaker.TakerInterface import Taker
from Requests.RequestGeneratorInterface import RequestGenerator
from Responses.ResponseGeneratorInterface import ResponseGenerator


class TwistedTaker(Taker, resource.Resource):
    isLeaf = True

    def __init__(self, request_generator: RequestGenerator, response_generator: ResponseGenerator, forwarder):
        Taker.__init__(self, request_generator, response_generator, forwarder)
        resource.Resource.__init__(self)

    def render_GET(self, request):
        print("GET request", request.content.read().decode("utf-8"))
        return bytes("work", "utf-8")

    def render_POST(self, request):
        data = request.content.read().decode("utf-8")
        loaded_data = json.loads(data)
        # try:
        response = self.take(loaded_data)
        # except Exception as e:
        #     response = "internal error:\n\t" + str(e)
        print("\nPOST:", data, "\n", response, "\n")
        response = json.dumps(response)
        return bytes(response, "utf-8")

    def start(self):
        site = server.Site(self)
        reactor.listenTCP(8080, site)
        return reactor.run()

    def stop(self):
        reactor.stop()
