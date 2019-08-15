import sqlite3

import os
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


def fields_names_to_str(values):
    raw_fields = list(values.keys())
    str_fields = ""
    for i in range(len(raw_fields)):
        str_fields += raw_fields[i]
        if i != len(raw_fields) - 1:
            str_fields += ", "
    return str_fields


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


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def without(d, key):
    new_d = d.copy()
    new_d.pop(key)
    return new_d


class SqlLiteWorker(DataWorker):
    def __init__(self, table):
        self.table = table
        self.conn = None

    def prepare(self):
        first_file_path = os.path.join(os.getcwd(), os.listdir(os.getcwd())[0])
        sql_path = os.path.dirname(first_file_path) + '\\data\\new_file'

        try:
            self.conn = sqlite3.connect(sql_path)
        except sqlite3.Error as e:
            print(e.args)

        self.conn.row_factory = dict_factory
        return True

    def insert(self, values: {}):
        cur = self.conn.cursor()

        cur.execute("""INSERT INTO {}({}) VALUES ({})""".format(
            self.table,
            fields_names_to_str(values),
            fields_values_to_str(values)
        ))

        self.conn.commit()

        return cur.rowcount == 1

    def select(self, values: {}):
        cur = self.conn.cursor()

        conditions = convert_conditions_to_text(values)

        cur.execute("""SELECT * from {}{}""".format(
            self.table,
            " where " + conditions if conditions else ""
        ))

        raw_rows = cur.fetchmany()
        cleared_rows = del_empty_fields(raw_rows)
        return cleared_rows

    def delete(self, values: {}):
        cur = self.conn.cursor()

        cur.execute("""DELETE FROM {} WHERE {}""".format(
            self.table,
            convert_conditions_to_text(values)
        ))
        self.conn.commit()

        return cur.rowcount == 1

    def update(self, values: {}):
        cur = self.conn.cursor()

        cur.execute("""UPDATE {} SET {} WHERE {}""".format(
            self.table,
            convert_conditions_to_text(without(values, "id")),
            convert_conditions_to_text({"id": values["id"]})
        ))

        self.conn.commit()
        return cur.rowcount == 1


