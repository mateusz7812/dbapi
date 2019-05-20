from Managers.ManagerInterface import Manager


class DataBaseManager(Manager):

    def __init__(self):
        super().__init__()

    def manage(self, action, data):
        if action == "add":
            return self.writers[list(self.writers.keys())[0]].insert(data)
        elif action == "get":
            return self.writers[list(self.writers.keys())[0]].select(data)
        elif action == "del":
            return self.writers[list(self.writers.keys())[0]].delete(data)
        raise Exception("action not found")
