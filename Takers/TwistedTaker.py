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
            print("ERROR", "POST request", data)
            raise exc
        if print_results:
            print("POST request", data, "\n response", response)
            sys.stdout.flush()
        response = json.dumps(response)

        request.setHeader('Access-Control-Allow-Origin', '*')

        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'POST')
        request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with')
        request.setHeader('Access-Control-Max-Age', 2520)  # 42 hours

        # normal JSON header
        request.setHeader('Content-type', 'application/json')
        request.write(bytes(response, "utf-8"))  # gotta use double-quotes in JSON apparently
        request.finish()

        # return this even though the request really is finished by now
        return server.NOT_DONE_YET

        ##return bytes(response, "utf-8")

    def start(self):
        site = server.Site(self)
        reactor.listenTCP(7000, site)
        return reactor.run()

    def stop(self):
        reactor.stop()
