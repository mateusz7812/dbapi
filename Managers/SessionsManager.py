from Managers.ManagerInterface import Manager


class SessionsManager(Manager):
    def manage(self, action, data):
        if action == "add":
            return self.writers["sessions"].insert(data)
        elif action == "get":
            return self.writers["sessions"].select(data)
        elif action == "del":
            return self.writers["sessions"].delete(data)
        raise Exception("action not found")
