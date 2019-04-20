from RequestsForwarder.ForwarderInterface import Forwarder


class BasicForwarder(Forwarder):
    def forward(self, response):
        processor = self.find_processor(response)
        result = processor.process(response)
        return result

    def find_processor(self, response):
        for processor in self.processors:
            if processor.name == response.request.object.type:
                return processor
        return None

