class TaskForwarder:
    def __init__(self, listsP=None, usersP=None):
        self.listP = listsP
        self.userP = usersP

    def forward(self, request):
        object = request.pop("object")
        if object == "user":
            return self.forward_user(request)
        elif object == "list":
            return self.forward_list(request)
        else:
            return {"info": "object not found"}

    def forward_list(self, request):
        action = request.pop("action")
        if action == "get":
            return self.listP.get(request)
        elif action == "add":
            return self.listP.add(request)
        elif action == "del":
            return self.listP.delete(request)
        elif action == "edit":
            return self.listP.edit(request)
        else:
            return {"info": "action not found"}

    def forward_user(self, request):
        action = request.pop("action")
        if action == "login":
            return self.userP.login(request)
        elif action == "logout":
            return self.userP.logout(request)
        elif action == "reg":
            return self.userP.register(request)
        elif action == "delete":
            return self.userP.delete(request)
        else:
            return {"info": "action not found"}
