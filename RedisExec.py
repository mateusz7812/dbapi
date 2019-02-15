import redis


class RExecutor:
    def __init__(self):
        self.password = self.get_pass()

        self.redis = redis.Redis(
            host='localhost',
            port='6379',
            password=self.password
        )

    def get_pass(self):
        with open("rpass") as f:
            data = f.readline()
        return data

    def __get__(self, instance, owner):
        return self.redis
