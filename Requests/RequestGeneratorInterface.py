class RequestGenerator:
    def __init__(self, forwarders: []):
        self.forwarders = forwarders

    def generate_request(self, data):
        raise NotImplementedError
