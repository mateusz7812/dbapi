
from DBManager import DBListManager, DBListMBase
from DataProcessor import DataProcessor, SessionManager


class BaseBranch:
    name: str = None

    def process_request(self, task):
        raise NotImplementedError


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

    def __init__(self, UDManager: DataProcessor = DataProcessor):
        self.UDManager = UDManager

    def process_request(self, task):
        self.UDManager = self.UDManager(task)
        return self.UDManager.add()


class UserDel(BaseBranch):
    name = "del"

    def __init__(self, UManager: DataProcessor = DataProcessor):
        self.UManager = UManager

    def process_request(self, task):
        self.UManager = self.UManager(task)
        return self.UManager.delete()


class UserLogin(BaseBranch):
    name = "login"

    def __init__(self, SManager: SessionManager = SessionManager):
        self.SManager = SManager

    def process_request(self, task):
        self.SManager = self.SManager(task)
        return self.SManager.add()


class UserLogout(BaseBranch):
    name = "logout"

    def __init__(self, SManager: SessionManager = SessionManager):
        self.SManager = SManager

    def process_request(self, task):
        self.SManager = self.SManager(task)
        return self.SManager.delete()


class ListsBranch(BaseBranch):
    name = "list"

    def __init__(self, Rmanager):
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
        return self.DBmanager.add


class ListDel(BaseBranch):
    name = "del"

    def __init__(self, DBmanager: DBListMBase = DBListManager):
        self.DBmanager = DBmanager

    def process_request(self, task):
        self.DBmanager = self.DBmanager(task)
        return self.DBmanager.delete()


