from multiprocessing import Process

from RequestsForwarder.ForwarderInterface import Forwarder
from RequestTaker.TakerInterface import Taker


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
    program = Main()
    program.start()
