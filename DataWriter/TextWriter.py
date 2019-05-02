import json

from DataWriter.WriterInterface import Writer


def match(values, line):
    for key in values.keys():
        if line[key] != values[key]:
            return False
    return True


class TextWriter(Writer):
    def insert(self, values: {}):
        with open(self.table, "a") as file:
            file.write(json.dumps(values) + "\n")
        return True

    def select(self, values: {}):
        with open(self.table, "r") as file:
            all_lines = [json.loads(line[:-1]) for line in file.readlines()]
        return list(filter(lambda x: match(values, x), all_lines))

    def delete(self, values: {}):
        cleared_data = []
        deleted_data = []

        with open(self.table, "r") as file:
            all_lines = [json.loads(line[:-1]) for line in file.readlines()]

        for line in all_lines:
            if match(values, line):
                deleted_data.append(line)
            else:
                cleared_data.append(line)

        with open(self.table, "w") as file:
            for data in cleared_data:
                file.write(json.dumps(data) + "\n")
        return deleted_data
