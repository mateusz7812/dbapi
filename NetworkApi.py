import json

from twisted.web import resource
from Branchs import TaskHandler, BaseHandler


class NetApi(resource.Resource):
    isLeaf = True

    def __init__(self, handler: BaseHandler = TaskHandler):
        super().__init__()
        self.processer = handler

    def render_GET(self, request):
        print("GET request", request.content.read())
        return True

    def render_POST(self, request):
        data = request.content.read().decode("utf-8")
        print("POST request", request.content.read())
        task = json.loads(data)
        try:
            self.processer = self.processer()
            response = self.processer.process_request(task)
        except Exception as e:
            response = "internal error:\n\t" + str(e)
        print("response: ", response)
        return bytes(response, "utf-8") if type(response) != bytes else response

if __name__ == "__main__":
    from twisted.internet import reactor
    from twisted.web import server

    site = server.Site(NetApi())
    reactor.listenTCP(8080, site)
    reactor.run()
