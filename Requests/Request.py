from Requests.RequestInterface import Request


class Request(Request):
    def __init__(self, account: {}, data_object: {}, action: str):
        super().__init__(account, data_object, action)
