from abc import ABC


class BaseBranch:
    name: str = None

    def process_request(self, task):
        raise NotImplementedError


class ManagerBase:
    def add(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class RedisMBase(ManagerBase, ABC):
    def __init__(self, user_id: int):
        self.user_id: int = user_id
        self.user_key: str = ""


class DBUserMBase(ManagerBase, ABC):
    def __init__(self, data: []):
        self.login: str = data[0]
        self.password: str = data[1]
        self.data: [] = data[2:]


class DBListMBase(ManagerBase, ABC):
    def __init__(self, data: []):
        self.user_id: int = data[0]
        self.user_key: str = data[1]
        self.data: [] = data[2:]



