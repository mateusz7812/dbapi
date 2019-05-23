from Requests.RequestInterface import Request


class BasicRequest(Request):
    def __init__(self, account: {}, data_object: {}, action: str):
        super().__init__(account, data_object, action)
