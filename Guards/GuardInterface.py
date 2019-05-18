
class Guard:
    authorization_methods = []

    def resolve(self, response):
        raise NotImplementedError
