import json

from twisted.web import resource
from twisted.internet import reactor
from twisted.web import server


class HttpApi(resource.Resource):
    isLeaf = True

    def __init__(self, forwarder):
        super().__init__()
        self.forwarder = forwarder

    def render_GET(self, request):
        print("GET request", request.content.read().decode("utf-8"))
        return bytes("work", "utf-8")

    def render_POST(self, request):
        data = request.content.read().decode("utf-8")
        task = json.loads(data)
        try:
            response = self.forwarder.forward(task)
        except Exception as e:
            response = "internal error:\n\t" + str(e)
        print("\nPOST:", data, "\n", response, "\n")
        response = json.dumps(response)
        return bytes(response, "utf-8")

    def run(self):
        site = server.Site(self)
        reactor.listenTCP(8080, site)
        return reactor.run()

    def stop(self):
        reactor.stop()
