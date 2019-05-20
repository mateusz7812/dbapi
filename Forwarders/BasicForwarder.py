from Forwarders.ForwarderInterface import Forwarder


class BasicForwarder(Forwarder):
    def __init__(self, response_generator, guard):
        self.guard = guard()
        super().__init__(response_generator)

    def forward(self, request):
        response = self.response_generator.generate(request)

        if not self.guard.resolve(response):
            response.result["status"] = "failed"
            response.result["error"] = "not authorized"
            return response.result

        return self.get_results(request)

    def get_results(self, request):
        response = self.response_generator.generate(request)

        processor = self.find_processor(response)

        required_requests = processor.get_required_requests(response)
        for required_request in required_requests:
            result_required = self.get_results(required_request)
            response.request.required[required_request.object["type"]] = result_required

        response = processor.process(response)
        response.result["status"] = response.status
        return response.result

    def add_processor(self, processor):
        self.processors[processor.name] = processor
        self.guard.add_processor(processor)

    def find_processor(self, response):
        try:
            return self.processors[response.request.object["type"]]
        except KeyError:
            raise Exception("No processor with such name")

