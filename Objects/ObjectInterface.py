class Object:
    def __init__(self, object_type, object_data):
        self.type: str = object_type
        self.data: {} = object_data

    def validate(self):
        raise NotImplementedError
