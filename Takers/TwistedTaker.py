import json
import sys
import traceback

from twisted.web import resource
from twisted.internet import reactor
from twisted.web import server

from Takers.TakerInterface import Taker

print_results = True


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
        try:
            response = self.take(loaded_data)
        except Exception as exc:
            traceback.print_exception(type(exc), exc, exc.__traceback__)
            print("ERROR", "POST request", data)
            sys.stdout.flush()
            return bytes(json.dumps({"error": "internal"}), "utf-8")
        if print_results:
            print("POST request", data, "\n response", response)
            sys.stdout.flush()
        response = json.dumps(response)
        return bytes(response, "utf-8")

    def start(self):
        site = server.Site(self)
        reactor.listenTCP(7000, site)
        return reactor.run()

    def stop(self):
        reactor.stop()
