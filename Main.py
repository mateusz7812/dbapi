from WriteManager.DBManager import UsersDBManager, ListsDBManager
from DataWriter.DataBaseExecutors import TextBExecutor
from ObjectForwarder.Forwarder import TaskForwarder
from RequestTaker.Http import HttpApi
from TaskProcessor.Processor import UsersProcessor, ListsProcessor
from WriteManager.SessionManager import SessionManager
from DataWriter.TempDataExecutors import TextTempExecutor

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
