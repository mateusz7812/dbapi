import json

from twisted.web import resource
from Branchs import TaskHandler, BaseHandler
from twisted.internet import reactor
from twisted.web import server


class HttpApi(resource.Resource):
    isLeaf = True

    def __init__(self, handler: BaseHandler = TaskHandler):
        super().__init__()
        self.taskHandler = handler
        self.taskHandler = self.taskHandler()

    def render_GET(self, request):
        print("GET request", request.content.read())
        return bytes("work", "utf-8")

    def render_POST(self, request):
        data = request.content.read().decode("utf-8")
        print("POST request", request.content.read())
        task = json.loads(data)
        "try:"
        self.taskHandler = self.taskHandler()
        response = self.taskHandler.process_request(task)
        """except Exception as e:
            response = "internal error:\n\t" + str(e)"""
        print("response: ", response)
        if type(response) == bool:
            response = str(response)
        if type(response) == str:
            return bytes(response, "utf-8")
        raise Exception("bad return type", response)

    def run(self):
        site = server.Site(HttpApi())
        reactor.listenTCP(8080, site)
        reactor.run()
