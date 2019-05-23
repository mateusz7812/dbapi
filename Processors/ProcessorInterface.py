from Requests.RequestInterface import Request
from Managers.ManagerInterface import Manager


class Processor:
    name: str
    authorization_rules = {}

    def __init__(self, manager=None):
        self.manager = manager

    def process(self, response):
        raise NotImplementedError
