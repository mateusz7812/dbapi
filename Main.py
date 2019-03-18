from DBManager import UsersDBManager, ListsDBManager
from DataBaseExecutors import TextBExecutor
from Forwarder import TaskForwarder
from HttpApi import HttpApi
from Processor import UsersProcessor, ListsProcessor
from SessionManager import SessionManager
from TempDataExecutors import TextTempExecutor

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

    processors = [usersP, listsP]
    forwarder = TaskForwarder(processors)

    HttpApi(forwarder).run()


if __name__ == "__main__":
    main()
