from unittest import TestCase

from Branchs import DBUserMBase, UserReg, UserLogin, RedisMBase, UserLogout, UserDel


class TestUserDBManager(DBUserMBase):
    def add(self):
        return ["add"] + self.data

    def get(self):
        if self.login == "test1" and self.password == "test2":
            return 12
        return False

    def delete(self):
        if self.get():
            return True
        return False


class TestRedisManager(RedisMBase):
    def add(self):
        return "key2"

    def get(self):
        if self.user_id == 12:
            return "key1"
        return False

    def delete(self):
        return self.get()


class TestUserBranch(TestCase):
    def test_UserReg(self):
        result = UserReg(TestUserDBManager).process_request(["test1", "test2", "nick"])
        self.assertEqual(result, ["add", "nick"])

    def test_UserLogin_correct(self):
        result = UserLogin(TestUserDBManager, TestRedisManager).process_request(["test1", "test2"])
        self.assertEqual(result, "key1")

    def test_UserLogin_bad_pass(self):
        result = UserLogin(TestUserDBManager, TestRedisManager).process_request(["other", "pass"])
        self.assertFalse(result)

    def test_UserLogout_correct(self):
        result = UserLogout(TestRedisManager).process_request([12, "key1"])
        self.assertTrue(result)

    def test_UserLogout_bad_key(self):
        result = UserLogout(TestRedisManager).process_request([12, "other"])
        self.assertFalse(result)

    def test_UserLogout_bad_id(self):
        result = UserLogout(TestRedisManager).process_request([10, "key1"])
        self.assertFalse(result)

    def test_UserDel_correct(self):
        result = UserDel(TestUserDBManager).process_request(["test1", "test2"])
        self.assertEqual(result, True)






