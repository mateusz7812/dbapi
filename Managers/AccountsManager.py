from Managers.ManagerInterface import Manager


class AccountsManager(Manager):
    def manage(self, action, data):
        if action == "add":
            return self.writers["accounts"].insert(data)
        elif action == "get":
            return self.writers["accounts"].select(data)
        elif action == "del":
            return self.writers["accounts"].delete(data)
        raise Exception("action not found")
