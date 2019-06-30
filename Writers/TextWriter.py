import json

from Writers.WriterInterface import DataWriter


def match(values, line):
    for key in values.keys():
        if line[key] != values[key]:
            return False
    return True


class TextWriter(DataWriter):
    def __init__(self, table):
        self.table = table

    def prepare(self):
        try:
            with open("data/"+self.table, "x") as _:
                return True
        except FileExistsError:
            return True
        except Exception:
            return False

    def insert(self, values: {}):
        if "id" not in values.keys():
            rows = self.select({})
            ids = list(map(lambda x: x["id"], rows))
            ids.append(0)
            values["id"] = max(ids) + 1
        with open("data/"+self.table, "a") as file:
            file.write(json.dumps(values) + "\n")
        return True

    def select(self, values: {}):
        with open("data/"+self.table, "r") as file:
            all_lines = [json.loads(line[:-1]) for line in file.readlines()]
        return list(filter(lambda x: match(values, x), all_lines))

    def delete(self, values: {}):
        cleared_data = []
        deleted_data = []

        with open("data/"+self.table, "r") as file:
            all_lines = [json.loads(line[:-1]) for line in file.readlines()]

        for line in all_lines:
            if match(values, line):
                deleted_data.append(line)
            else:
                cleared_data.append(line)

        with open("data/"+self.table, "w") as file:
            for data in cleared_data:
                file.write(json.dumps(data) + "\n")
        return deleted_data
