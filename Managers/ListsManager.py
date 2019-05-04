from Managers.ManagerInterface import Manager


class ListsManager(Manager):
    def manage(self, action, data):
        if action == "add":
            return self.writers["lists"].insert(data)
        elif action == "get":
            return self.writers["lists"].select(data)
        elif action == "del":
            return self.writers["lists"].delete(data)
        raise Exception("action not found")
