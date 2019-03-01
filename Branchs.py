from BranchInterfaces import BaseBranch, DBUserMBase, RedisMBase, DBListMBase
from RedisManager import RManager
from DBManager import DBUserManager, DBListManager


class BaseHandler:
    def process_request(self, data: str):
        raise NotImplementedError

    def __init__(self, rawBranchs: []):
        self.branchs = {}
        self.add_branchs(rawBranchs)

    def add_branchs(self, rawBranchs: []):
        for branch in rawBranchs:
            self.branchs[branch.name] = branch
        return self.branchs


class TaskHandler(BaseHandler):
    def __init__(self, branchs: [] = None):
        if branchs is None:
            branchs = [UserBranch, ListsBranch]
        super(TaskHandler, self).__init__(branchs)

    def process_request(self, data):
        branch = self.branchs[data[0]]()
        return branch.process_request(data[1:])


class UserBranch(BaseBranch):
    name = "user"

    def process_request(self, task):
        return TaskHandler([UserReg, UserDel, UserLogin, UserLogout]).process_request(task)


class UserReg(BaseBranch):
    name = "reg"

    def __init__(self, DBmanager: DBUserMBase = DBUserManager):
        self.DBmanager = DBmanager

    def process_request(self, task):
        self.DBmanager = self.DBmanager(task)
        return self.DBmanager.add()


class UserLogin(BaseBranch):
    name = "login"

    def __init__(self, DBmanager: DBUserMBase = DBUserManager, Rmanager: RedisMBase = RManager):
        self.DBmanager = DBmanager
        self.Rmanager = Rmanager

    def process_request(self, task):
        self.DBmanager = self.DBmanager(task)
        if not self.DBmanager.get():
            return False
        user_id = self.DBmanager.get()

        self.Rmanager = self.Rmanager(user_id)
        self.user_key = self.Rmanager.get()
        if self.user_key:
            return self.user_key

        return self.Rmanager.add()


class UserLogout(BaseBranch):
    name = "logout"

    def __init__(self, Rmanager: RedisMBase = RManager):
        self.Rmanager = Rmanager

    def process_request(self, task):
        self.Rmanager = self.Rmanager(task[0])
        if self.Rmanager.get() == task[1]:
            return self.Rmanager.delete()
        return False


class UserDel(BaseBranch):
    name = "del"

    def __init__(self, DBmanager: DBUserMBase = DBUserManager):
        self.DBmanager = DBmanager

    def process_request(self, task):
        self.DBmanager = self.DBmanager(task)
        if self.DBmanager.get():
            return self.DBmanager.delete()
        return False


class ListsBranch(BaseBranch):
    name = "list"

    def __init__(self, Rmanager: RedisMBase = RManager):
        self.Rmanager = Rmanager

    def process_request(self, task):
        self.Rmanager = self.Rmanager()
        task[1] = self.Rmanager.get_user_id(task[1])
        return TaskHandler([ListsGet, ListAdd, ListDel]).process_request(task)


class ListsGet(BaseBranch):
    name = "get"

    def __init__(self, DBmanager: DBListMBase = DBListManager):
        self.DBmanager = DBmanager

    def process_request(self, task):
        self.DBmanager = self.DBmanager(task)
        return self.DBmanager.get()


class ListAdd(BaseBranch):
    name = "add"

    def __init__(self, DBmanager: DBListMBase = DBListManager):
        self.DBmanager = DBmanager

    def process_request(self, task):
        self.DBmanager = self.DBmanager(task)
        return self.DBmanager.add()


class ListDel(BaseBranch):
    name = "del"

    def __init__(self, DBmanager: DBListMBase = DBListManager):
        self.DBmanager = DBmanager

    def process_request(self, task):
        self.DBmanager = self.DBmanager(task)
        return self.DBmanager.delete()


