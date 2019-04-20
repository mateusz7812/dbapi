class DataObject:
    def __init__(self, object_data):
        self.type: str = object_data["type"]
        self.data: {} = object_data
        del self.data["type"]
