import json
from multiprocessing import Process

from Takers.TakerInterface import Taker
from Writers.TextWriter import TextWriter


class FileTaker(Taker):
    read_process = None
    responses_writer = TextWriter("responses")
    requests_writer = TextWriter("requests")

    def taking_responses(self):
        old_requests = self.requests_writer.select({})
        while 1:
            all_requests = self.requests_writer.select({})
            new_requests = list(filter(lambda x: x not in old_requests, all_requests))
            if len(new_requests):
                request = new_requests[0]
                request_id = request["id"]
                data = json.loads(request["request"])
                response = self.take(data)
                self.responses_writer.insert({"id": request_id, "response": json.dumps(response)})
                old_requests.append(request)

    def start(self):
        if not self.responses_writer.prepare():
            raise Exception("responses file error")
        if not self.requests_writer.prepare():
            raise Exception("requests file error")
        self.read_process = Process(target=self.taking_responses)
        self.read_process.daemon = True
        self.read_process.start()

    def stop(self):
        self.read_process.terminate()
