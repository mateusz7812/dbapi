from RequestsForwarder.ForwarderInterface import Forwarder


class BasicForwarder(Forwarder):
    def forward(self, request):
        response = self.response_generator.generate(request)
        processor = self.find_processor(response)
        required_requests = processor.get_required_requests(response)
        for required_request in required_requests:
            result_required = self.forward(required_request)
            for key in result_required.keys():
                response.request.object[key] = result_required[key]
        response = processor.process(response)
        response.result["status"] = response.status
        return response.result

    def find_processor(self, response):
        for processor in self.processors:
            if processor.name == response.request.object["type"]:
                return processor
        raise Exception("No processor with such name")

