from Requests.RequestInterface import Request
from WriteManager.ManagerInterface import Manager


class Processor:
    def __init__(self, name):
        self.name = name
        self.managers = []

    def add_manager(self, manager: Manager):
        self.managers.append(manager)

    def process(self, response):
        raise NotImplementedError

    def get_required_requests(self, response):
        raise NotImplementedError
