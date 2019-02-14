import redis


class RExecutor:
    def __init__(self):
        self.redis = redis.Redis(
            host='localhost',
            port='6379',
            password=''
        )

    def __get__(self, instance, owner):
        return self.redis
