from Managers.ManagerInterface import Manager


class EmailManager(Manager):

    def __init__(self):
        super().__init__()

    def manage(self, action, data):
        if action == "send":
            return self.writers[list(self.writers.keys())[0]].send(data)
        raise Exception("action not found")

