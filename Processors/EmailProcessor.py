import copy

from Processors.ProcessorInterface import Processor


class EmailProcessor(Processor):
    name = "email"

    authorization_rules = {
        "send": {"anonymous": [], "account": [], "session": [], "admin": [{"message"}]}
    }

    def process(self, response):
        data = copy.deepcopy(response.request.object)
        data.pop("type")

        response.result["objects"] = self.manager.manage(response.request.action, data)
        response.status = "handled"
        return response
