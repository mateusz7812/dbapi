import random
from twisted.web import server, resource
from twisted.internet import reactor
import json
from DBExec import register, login, add_list, del_list, get_lists
from RedisExec import RExecutor


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
    user_key = random.randInt(0, 1000000)
    with RExecutor() as exc:
        exc.set(user_key, user_id)
    return user_key


def list_manager(task):
    kind = task[0]
    if kind == "get":
        user_id = get_user_id(task[1:])
        return get_lists(user_id)
    elif kind == "add":
        return add_list(task[1:])
    elif kind == "del":
        return del_list(task[1:])


def get_user_id(user_key):
    with RExecutor() as exc:
        user_id = exc.get(user_key)
    return user_id


class netApi(resource.Resource):
    isLeaf = True

    def render_POST(self, request):
        task = json.loads(request.content.read())
        return bytes(process_request(task), "utf-8")

if __name__ == "__main__":
    site = server.Site(netApi())
    reactor.listenTCP(8080, site)
    reactor.run()
