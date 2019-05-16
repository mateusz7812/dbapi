import json

from twisted.web import resource
from twisted.internet import reactor
from twisted.web import server

from Takers.TakerInterface import Taker

print_results = False


class TwistedTaker(Taker, resource.Resource):
    isLeaf = True

    def __init__(self, request_generator, forwarder):
        Taker.__init__(self, request_generator, forwarder)
        resource.Resource.__init__(self)

    def render_GET(self, request):
        if print_results:
            print("GET request", request.content.read().decode("utf-8"))
        return bytes("work", "utf-8")

    def render_POST(self, request):
        data = request.content.read().decode("utf-8")
        loaded_data = json.loads(data)
        response = self.take(loaded_data)
        if print_results:
            print("\nPOST request", data, "\n response", response, "\n")
        response = json.dumps(response)
        return bytes(response, "utf-8")

    def start(self):
        site = server.Site(self)
        reactor.listenTCP(8080, site)
        return reactor.run()

    def stop(self):
        reactor.stop()
