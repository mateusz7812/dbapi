from twisted.web import server, resource
from twisted.internet import reactor


class Simple(resource.Resource):
    isLeaf = True

    def render_POST(self, request):
        return request.content.read()

if __name__ == "__main__":
    site = server.Site(Simple())
    reactor.listenTCP(8080, site)
    reactor.run()
