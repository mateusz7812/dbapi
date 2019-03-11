from DBManager import TextBExecutor, UsersDBManager
from HttpApi import HttpApi

DataWriter = TextBExecutor()
UserDataManager = UsersDBManager()


def main():

    HttpApi().run()


if __name__ == "__main__":
    main()
