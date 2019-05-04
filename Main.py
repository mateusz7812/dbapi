from multiprocessing import Process

from Forwarders.BasicForwarder import BasicForwarder
from Forwarders.ForwarderInterface import Forwarder
from Managers.AccountsManager import AccountsManager
from Managers.ListsManager import ListsManager
from Processors.AccountProcessor import AccountProcessor
from Processors.ListProcessor import ListProcessor
from Requests.RequestGeneratorBasic import BasicRequestGenerator
from Responses.BasicResponseGenerator import BasicResponseGenerator
from Takers.TakerInterface import Taker
from Takers.TwistedTaker import TwistedTaker
from Writers.TextWriter import TextWriter


class Main:
    def __init__(self, takers: []):
        self.takers = takers
        self.started_takers = []
        self.check_types()

    def check_types(self):
        for x in self.takers:
            if not issubclass(x.__class__, Taker):
                raise TypeError

    def start(self):
        for taker in self.takers:
            server = Process(target=taker.start)
            server.start()
            self.started_takers.append(server)

    def stop(self):
        for taker in self.started_takers:
            taker.terminate()


if __name__ == "__main__":
    requestGenerator = BasicRequestGenerator
    responseGenerator = BasicResponseGenerator
    forwarder = BasicForwarder(responseGenerator)

    account_processor = AccountProcessor(requestGenerator)
    account_manager = AccountsManager()
    accounts_writer = TextWriter("accounts")
    account_manager.add_writer(accounts_writer)
    account_processor.add_manager(account_manager)
    forwarder.add_processor(account_processor)

    list_processor = ListProcessor(requestGenerator)
    lists_manager = ListsManager()
    lists_writer = TextWriter("lists")
    lists_manager.add_writer(lists_writer)
    list_processor.add_manager(lists_manager)
    forwarder.add_processor(list_processor)

    taker = TwistedTaker(requestGenerator, forwarder)
    program = Main([taker])
    program.start()
