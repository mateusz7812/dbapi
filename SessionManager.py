from abc import ABC

import redis


class SessionExecutorBase:
    def add(self, data):
        raise NotImplementedError

    def get(self, data):
        raise NotImplementedError

    def delete(self, data):
        raise NotImplementedError


class SessionManager:
    def __init__(self, SExecutor):
        self.SExecutor = SExecutor

    def add(self, data):
        if self.SExecutor.add(data):
            return {"info": "session added", "user_id": data[0], "user_key": data[1]}
        else:
            return {"info": "session not added"}

    def get(self, data):
        if self.SExecutor.get(data):
            return {"info": "session correct"}
        else:
            return {"info": "session not correct"}

    def delete(self, data):
        data_correct = self.get(data)["info"]
        if data_correct == "session correct":
            if self.SExecutor.delete(data):
                return {"info": "session deleted"}
            return {"info": "session not deleted"}
        return {"info": data_correct}
