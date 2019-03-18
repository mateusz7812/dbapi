from managers.DBManager import UsersDBManager, ListsDBManager
from writers.DataBaseExecutors import TextBExecutor
from net_Interface.Forwarder import TaskForwarder
from net_Interface.HttpApi import HttpApi
from Processor import UsersProcessor, ListsProcessor
from managers.SessionManager import SessionManager
from writers.TempDataExecutors import TextTempExecutor

DataWriter = TextBExecutor()
UserDataManager = UsersDBManager(DataWriter)


def main():
    dataWriter = TextBExecutor()
    usersDBM = UsersDBManager(dataWriter)
    listsDBM = ListsDBManager(dataWriter)

    sessionWriter = TextTempExecutor()
    sessionsM = SessionManager(sessionWriter)

    usersP = UsersProcessor(usersDBM, sessionsM)
    listsP = ListsProcessor(listsDBM, sessionsM)

    forwarder = TaskForwarder(usersP=usersP, listsP=listsP)

    HttpApi(forwarder).run()


if __name__ == "__main__":
    main()
