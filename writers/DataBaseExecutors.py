import json
import psycopg2
import os

from managers.DBManager import BaseDExecutor

cur_dir = os.path.dirname(os.path.abspath(__file__))
cur_dir = "\\".join(cur_dir.split("\\")[:-1])


class TextBExecutor(BaseDExecutor):
    def read_columns_names(self, tableName):
        with open(cur_dir + "\\textDataBases\\" + tableName, "r") as f:
            config = f.readline()
        config.replace("\n", "")
        return json.loads(config)

    def read_data(self, tableName):
        with open(cur_dir + "\\textDataBases\\" + tableName, "r") as f:
            raw_data = f.readlines()[1:]
        data = [json.loads(row[:-1]) for row in raw_data]
        return data

    def get_last_id(self, tableName):
        with open(cur_dir + "\\textDataBases\\" + tableName, "r") as f:
            data = f.readlines()
            data = data[-1]
        id = json.loads(data)[0]
        if id == "id":
            return 0
        return id

    def add(self, tableName, requestData: {}):
        if "id" in requestData.keys():
            if self.get_last_id(tableName) >= requestData["id"]:
                return []
        else:
            requestData["id"] = int(self.get_last_id(tableName)) + 1
        columns = self.read_columns_names(tableName)
        row = []
        for cell in columns:
            if cell in requestData.keys():
                row.append(requestData[cell])
            else:
                row.append(None)
        with open(cur_dir + "\\textDataBases\\" + tableName, "a") as f:
            f.write(json.dumps(row) + "\n")
        dict_row = {}
        for cell in columns:
            dict_row[cell] = row[columns.index(cell)]
        return dict_row

    def get(self, tableName, requestData):
        columns = self.read_columns_names(tableName)
        data_table = self.read_data(tableName)
        for key in requestData.keys():
            data_table = list(filter(lambda row: row[columns.index(key)] == requestData[key], data_table))
        dict_table = []
        for row in data_table:
            dict_row = {}
            for col in columns:
                dict_row[col] = row[columns.index(col)]
            dict_table.append(dict_row)
        return dict_table

    def delete(self, tableName, requestData):
        dicts_to_delete = self.get(tableName, requestData)
        lists_to_delete = [list(row.values()) for row in dicts_to_delete]

        all_rows = self.read_data(tableName)
        to_save = [self.read_columns_names(tableName)]
        to_save.extend(list(filter(lambda row: row not in lists_to_delete, all_rows)))

        with open(cur_dir + "\\textDataBases\\" + tableName, "w") as f:
            for row in to_save:
                row = json.dumps(row) + "\n"
                f.write(row)
        return dicts_to_delete


class PostgresExecutor(BaseDExecutor):
    def __init__(self, table, data):
        super(PostgresExecutor, self).__init__(table, data)
        [self.address, self.user, self.password] = self.get_pass()
        self.conn = None
        self.cur = None

    def open_connection(self, config):
        self.conn = psycopg2.connect(host=self.address, database="lists", user=self.user,
                                     password=self.password)
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.conn.commit()
        self.cur.close()
        self.cur = None
        self.conn.close()
        self.conn = None

    def get_pass(self):
        import os
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        with open(cur_dir + "\pass\dbpass") as f:
            data = f.readlines()
        data = [x[:-1].split(":") for x in data]
        for row in data:
            if row[0] == "lists":
                return row[1:]

    def add(self, tableName, data):
        fields = ", ".join(self.data.keys())
        values = [json.dumps(value).replace("\"", "\'") for value in self.data.values()]
        values = ", ".join(values)
        self.open_connection()
        self.cur.execute('SELECT id FROM {} order by id DESC LIMIT 1'.format(self.tableName))
        last_id = self.cur.fetchone()
        if last_id and "id" in self.data.keys():
            if last_id[0] > self.data["id"]:
                return []
        self.cur.execute('INSERT INTO {0}({1}) VALUES({2}) RETURNING *'.format(self.tableName, fields, values))
        result = self.cur.fetchone()
        self.close_connection()
        return list(result)

    def get(self, tableName, data):
        fields = list(self.data.keys())
        values = list(self.data.values())
        values = [json.dumps(value).replace("\"", "\'") for value in values]
        conditions = ["{}={}".format(fields[x], values[x]) for x in range(len(fields))]
        conditions = " AND ".join(conditions)
        self.open_connection()
        self.cur.execute('SELECT * FROM {0} WHERE {1}'.format(self.tableName, conditions))
        result = self.cur.fetchall()
        self.close_connection()
        return list(map(list, result))

    def delete(self, tableName, data):
        fields = list(self.data.keys())
        values = list(self.data.values())
        values = [json.dumps(value).replace("\"", "\'") for value in values]
        conditions = ["{}={}".format(fields[x], values[x]) for x in range(len(fields))]
        conditions = " AND ".join(conditions)
        self.open_connection()
        self.cur.execute('DELETE FROM {0} WHERE {1} RETURNING *'.format(self.tableName, conditions))
        deleted = self.cur.fetchall()
        self.close_connection()
        return list(map(list, deleted))

