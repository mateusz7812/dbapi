from unittest import TestCase

from Branchs import UserReg, UserLogin, UserLogout, UserDel
from DataProcessor import DataManagerBase


class TestUserDataManager(DataManagerBase):
    def __init__(self, data):
        self.data = data

    def add(self):
        return ["adduser"] + self.data

    def delete(self):
        return ["deleteuser"] + self.data


class TestSessionManager(DataManagerBase):
    def __init__(self, data):
        self.data = data

    def add(self):
        return ["addsession"] + self.data

    def delete(self):
        return ["deletesession"] + self.data


class TestUserBranch(TestCase):
    def test_UserReg(self):
        result = UserReg(TestUserDataManager).process_request(["test1", "test2", "nick"])
        self.assertEqual(result, ["adduser", "test1", "test2", "nick"])

    def test_UserLogin(self):
        result = UserLogin(TestSessionManager).process_request(["test1", "test2"])
        self.assertEqual(result, ["addsession", "test1", "test2"])

    def test_UserLogout(self):
        result = UserLogout(TestSessionManager).process_request([12, "key1"])
        self.assertEqual(result, ["deletesession", 12, "key1"])

    def test_UserDel(self):
        result = UserDel(TestUserDataManager).process_request(["test1", "test2"])
        self.assertEqual(result, ["deleteuser", "test1", "test2"])






