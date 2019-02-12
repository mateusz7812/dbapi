import random

import redis
from twisted.web import server, resource
from twisted.internet import reactor
import json
from DBExec import register, login


def process_request(task):
    if task[0] == 'user':
        return user_manager(task[1:])
    elif task[0] == 'list':
        return list_manager(task[1:])


def user_manager(task):
    kind = task[0]
    if kind == "register":
        return register(task[1:])
    elif kind == "login":
        user_id = login(task[1:])
        if user_id != -1:
            return save_client(user_id)
        return False


def save_client(user_id: int):
    r = redis.Redis(
        host='localhost',
        port='6379',
        password=''
    )
    user_key = random.randInt(0, 1000000)
    r.set(user_id, user_key)
    return user_key


def list_manager(task):
    kind = task[0]
    if kind == "add":
        add_list(task[1:])
    elif kind == "del":
        del_list(task[1:])


class netApi(resource.Resource):
    isLeaf = True

    def render_POST(self, request):
        task = json.loads(request.content.read())
        return bytes(process_request(task), "utf-8")

if __name__ == "__main__":
    site = server.Site(netApi())
    reactor.listenTCP(8080, site)
    reactor.run()
