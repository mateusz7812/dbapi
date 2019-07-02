from multiprocessing import Process

from Forwarders.Forwarder import Forwarder
from Guards.Authorizer import Authorizer
from Managers.DataBaseManager import DataBaseManager
from Managers.DividedDataBaseManager import DividedDataBaseManager
from Managers.EmailManager import EmailManager
from Processors.AccountProcessor import AccountProcessor
from Processors.EmailProcessor import EmailProcessor
from Processors.FollowingProcessor import FollowingProcessor
from Processors.GroupProcessor import GroupProcessor
from Processors.ListProcessor import ListProcessor
from Processors.SessionProcessor import SessionProcessor
from Requests.RequestGenerator import RequestGenerator
from Responses.ResponseGenerator import ResponseGenerator
from Takers.TakerInterface import Taker
from Takers.TwistedTaker import TwistedTaker
from Writers.EmailWriter import EmailWriter
from Writers.PostgresWriter import PostgresWriter
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
        print("started")

    def stop(self):
        for taker in self.started_takers:
            taker.terminate()
        print("stopped")


if __name__ == "__main__":
    requestGenerator = RequestGenerator
    responseGenerator = ResponseGenerator
    guard = Authorizer
    forwarder = Forwarder(responseGenerator, guard)

    account_processor = AccountProcessor()
    account_manager = DataBaseManager()
    accounts_writer = PostgresWriter("postgres", "postgres", "postgres", "zaq1@WSX", "accounts")
    account_manager.add_writer(accounts_writer)
    account_processor.manager = account_manager
    forwarder.add_processor(account_processor)

    list_processor = ListProcessor()
    lists_manager = DataBaseManager()
    lists_writer = PostgresWriter("postgres", "postgres", "postgres", "zaq1@WSX", "lists")
    lists_manager.add_writer(lists_writer)
    list_processor.manager = lists_manager
    forwarder.add_processor(list_processor)

    session_processor = SessionProcessor()
    sessions_manager = DataBaseManager()
    sessions_writer = PostgresWriter("postgres", "postgres", "postgres", "zaq1@WSX", "sessions")
    sessions_manager.add_writer(sessions_writer)
    session_processor.manager = sessions_manager
    forwarder.add_processor(session_processor)

    following_processor = FollowingProcessor()
    following_manager = DividedDataBaseManager("following")
    following_account_writer = PostgresWriter("postgres", "postgres", "postgres", "zaq1@WSX", "follow_account")
    following_list_writer = PostgresWriter("postgres", "postgres", "postgres", "zaq1@WSX", "follow_list")
    following_group_writer = PostgresWriter("postgres", "postgres", "postgres", "zaq1@WSX", "follow_group")
    following_manager.add_writer(following_account_writer)
    following_manager.add_writer(following_list_writer)
    following_manager.add_writer(following_group_writer)
    following_processor.manager = following_manager
    forwarder.add_processor(following_processor)

    group_processor = GroupProcessor()
    group_manager = DataBaseManager()
    group_writer = PostgresWriter("postgres", "postgres", "postgres", "zaq1@WSX", "list_group")
    group_manager.add_writer(group_writer)
    group_processor.manager = group_manager
    forwarder.add_processor(group_processor)

    email_processor = EmailProcessor()
    email_manager = EmailManager()
    email_writer = EmailWriter()
    email_manager.add_writer(email_writer)
    email_processor.manager = email_manager
    forwarder.add_processor(email_processor)

    twisted_taker = TwistedTaker(requestGenerator, forwarder)
    program = Main([twisted_taker])
    program.start()
