from Managers.ManagerInterface import Manager


class DividedDataBaseManager(Manager):

    def __init__(self, dividing_column):
        super().__init__()
        self.dividing_column = dividing_column

    def manage(self, action, data):
        if action == "add":
            return self.writers[data.pop(self.dividing_column)].insert(data)
        elif action == "get":
            return self.writers[data.pop(self.dividing_column)].select(data)
        elif action == "del":
            return self.writers[data.pop(self.dividing_column)].delete(data)
        raise Exception("action not found")
