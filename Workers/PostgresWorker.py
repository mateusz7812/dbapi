import psycopg2
from psycopg2.extras import DictCursor

from Workers.WorkerInterface import DataWorker


def convert_conditions_to_text(values):
    conditions = ""
    for i in range(len(values)):
        key = list(values.keys())[i]
        if type(values[key]) == str:
            values[key] = "\'" + values[key] + "\'"
        conditions += "{} = {}".format(key, values[key])
        if i != len(values) - 1:
            conditions += " AND "
    return conditions


def del_empty_fields(raw_rows):
    cleared_rows = []
    if raw_rows:
        columns = list(raw_rows[0].keys())
        for row in raw_rows:
            cleared_row = {}
            for column in columns:
                if row[column]:
                    cleared_row[column] = row[column]
            cleared_rows.append(cleared_row)
    return cleared_rows


def fields_values_to_str(values):
    raw_fields = list(values.keys())
    str_values = ""
    for i in range(len(raw_fields)):
        if type(values[raw_fields[i]]) == str:
            values[raw_fields[i]] = "\'" + values[raw_fields[i]] + "\'"
        str_values += str(values[raw_fields[i]])
        if i != len(raw_fields) - 1:
            str_values += ", "
    return str_values


def fields_names_to_str(values):
    raw_fields = list(values.keys())
    str_fields = ""
    for i in range(len(raw_fields)):
        str_fields += raw_fields[i]
        if i != len(raw_fields) - 1:
            str_fields += ", "
    return str_fields


def without(d, key):
    new_d = d.copy()
    new_d.pop(key)
    return new_d


class PostgresWorker(DataWorker):
    def __init__(self, host, dbname, user, password, table):
        self.table = table
        self.password = password
        self.user = user
        self.dbname = dbname
        self.host = host
        self.conn = None

    def prepare(self):
        try:
            self.conn = psycopg2.connect(
                "dbname='{}' user='{}' host='{}' password='{}'".format(self.dbname, self.user, self.host,
                                                                       self.password))
            return True
        except psycopg2.Error:
            print("I am unable to connect to the database")
            return False

    def insert(self, values: {}):
        cur = self.conn.cursor(cursor_factory=DictCursor)

        cur.execute("""INSERT INTO {}({}) VALUES ({})""".format(
            self.table,
            fields_names_to_str(values),
            fields_values_to_str(values)
        ))

        self.conn.commit()

        return True

    def select(self, values: {}):
        cur = self.conn.cursor(cursor_factory=DictCursor)

        conditions = convert_conditions_to_text(values)

        cur.execute("""SELECT * from {}{}""".format(
            self.table,
            " where " + conditions if conditions else ""
        ))

        raw_rows = cur.fetchall()

        cleared_rows = del_empty_fields(raw_rows)
        return cleared_rows

    def delete(self, values: {}):
        cur = self.conn.cursor(cursor_factory=DictCursor)

        cur.execute("""DELETE FROM {} WHERE {} RETURNING *""".format(
            self.table,
            convert_conditions_to_text(values)
        ))

        self.conn.commit()

        raw_rows = cur.fetchall()
        return del_empty_fields(raw_rows)

    def update(self, values: {}):
        cur = self.conn.cursor(cursor_factory=DictCursor)

        cur.execute("""UPDATE {} SET {} WHERE {} RETURNING *""".format(
            self.table,
            convert_conditions_to_text(without(values, "id")),
            convert_conditions_to_text({"id": values["id"]})
        ))

        self.conn.commit()
        raw_rows = cur.fetchall()
        return del_empty_fields(raw_rows)
