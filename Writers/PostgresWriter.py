import json

import psycopg2
from psycopg2.extras import DictCursor

from Writers.WriterInterface import DataWriter


class PostgresWriter(DataWriter):
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

        raw_fields = list(values.keys())
        str_fields = ""
        for i in range(len(raw_fields)):
            str_fields += raw_fields[i]
            if i != len(raw_fields)-1:
                str_fields += ", "

        str_values = ""
        for i in range(len(raw_fields)):
            str_values += values[raw_fields[i]]
            if i != len(raw_fields)-1:
                str_values += ", "

        cur.execute("""INSERT INTO {}({}) VALUES ({})""".format(self.table, str_fields, str_values))
        self.conn.commit()

        return True

    def select(self, values: {}):
        cur = self.conn.cursor(cursor_factory=DictCursor)

        conditions = ""
        for i in range(len(values)):
            key = list(values.keys())[i]
            conditions += "{} = {}".format(key, values[key])
            if i != len(values)-1:
                conditions += " AND "
        if conditions:
            conditions = " where " + conditions

        cur.execute("""SELECT * from {}{}""".format(self.table, conditions))
        raw_rows = cur.fetchall()
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

    def delete(self, values: {}):
        cur = self.conn.cursor(cursor_factory=DictCursor)

        conditions = ""
        for i in range(len(values)):
            key = list(values.keys())[i]
            conditions += "{} = {}".format(key, values[key])
            if i != len(values)-1:
                conditions += " AND "

        cur.execute("""DELETE FROM {} WHERE {} RETURNING *""".format(self.table, conditions))
        self.conn.commit()
        raw_rows = cur.fetchall()
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
