from multiprocessing import Process

from ObjectForwarder.ForwarderInterface import Forwarder
from RequestTaker.TakerInterface import Taker
from Requests.RequestGeneratorInterface import RequestGenerator
from WriteManager.DBManager import UsersDBManager, ListsDBManager
from DataWriter.DataBaseExecutors import TextBExecutor
from ObjectForwarder.Forwarder import TaskForwarder
from RequestTaker.TwistedTaker import TwistedTaker
from TaskProcessor.Processor import UsersProcessor, ListsProcessor
from WriteManager.SessionManager import SessionManager
from DataWriter.TempDataExecutors import TextTempExecutor


class Main:
    def __init__(self, forwarders: [], takers: []):
        self.forwarders = forwarders
        self.takers = takers
        self.started_takers = []
        self.requestGenerator: RequestGenerator = None
        self.check_types()

    def check_types(self):
        for x in self.forwarders:
            if not issubclass(x, Forwarder):
                raise TypeError
        for x in self.takers:
            if not issubclass(x, Taker):
                raise TypeError

    def start(self):
        self.requestGenerator = RequestGenerator(self.forwarders)
        for taker in self.takers:
            server = Process(target=taker(self.requestGenerator).start)
            server.start()
            self.started_takers.append(server)

    def stop(self):
        for taker in self.started_takers:
            taker.terminate()


if __name__ == "__main__":
    program = Main()
    program.start()
