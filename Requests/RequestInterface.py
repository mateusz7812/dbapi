from Objects.DataObjectInterface import DataObject


class Request:
    def __init__(self, account: DataObject, data_object: DataObject, action: str):
        self.account = account
        self.object = data_object
        self.action = action



