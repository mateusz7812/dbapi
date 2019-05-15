import json
from multiprocessing import Process

from Takers.TakerInterface import Taker


class FileTaker(Taker):
    read_process = None

    def taking_responses(self):
        with open("data/requests") as f:
            last_line_number = len(f.readlines())
        while 1:
            with open("data/requests") as f:
                try:
                    new_line = f.read(last_line_number + 1)
                    if new_line == "":
                        continue
                    splitted = new_line.split(";")
                    request_id = int(splitted[0])
                    data = json.loads(splitted[1])
                    response = self.take(data)
                    with open("data/response", "a") as a:
                        a.write(str(request_id) + ";" + json.dumps(response) + "\n")
                    last_line_number += 1
                except EOFError:
                    pass

    def start(self):
        self.read_process = Process(target=self.taking_responses)
        self.read_process.start()

    def stop(self):
        self.read_process.terminate()
