from RequestsForwarder.ForwarderInterface import Forwarder


class BasicForwarder(Forwarder):
    def forward(self, request):
        response = self.response_generator.generate(request)
        processor = self.find_processor(response)
        requireds = processor.get_required_requests(response)
        for required in requireds:
            result_required = self.forward(required)
            print(result_required)
            for key in result_required.keys():
                response.request.object.data[key] = result_required[key]
        response = processor.process(response)
        return response.result

    def find_processor(self, response):
        for processor in self.processors:
            if processor.name == response.request.object.type:
                return processor
        raise Exception("No processor with such name")

