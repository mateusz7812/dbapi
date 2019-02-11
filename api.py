from twisted.web import server, resource
from twisted.internet import reactor
import json


class Simple(resource.Resource):
    isLeaf = True

    def process_request(self, task):
        if task[0] == 'user':
            return self.user_manager(task[1:])
        elif task[0] == 'list':
            return self.list_manager(task[1:])

    def user_manager(self, task):
        return json.dumps([task[0]])

    def list_manager(self, task):
        return json.dumps([task[0]])

    def render_POST(self, request):
        task = json.loads(request.content.read())
        return bytes(self.process_request(task), "utf-8")

if __name__ == "__main__":
    site = server.Site(Simple())
    reactor.listenTCP(8080, site)
    reactor.run()
