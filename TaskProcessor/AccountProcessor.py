import copy

from TaskProcessor.ProcessorInterface import Processor


class AccountProcessor(Processor):
    name = "account"

    def get_required_requests(self, response):
        if response.request.action == "add":
            return []
        elif response.request.action == "get":
            return []
        elif response.request.action == "del":
            required = self.request_generator.generate(
                {"account": {"type": "internal"}, "object": response.request.object, "action": "get"})
            return [required]

    def process(self, response):
        data = copy.deepcopy(response.request.object)
        data.pop("type")
        if "login" in data.keys() and "password" in data.keys():
            self.managers[0].manage(response.request.action, data)
            response.status = "handled"
        else:
            response.status = "failed"
            response.result["error"] = "no login/password"
        return response
