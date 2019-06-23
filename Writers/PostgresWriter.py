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
        pass

    def select(self, values: {}):
        cur = self.conn.cursor(cursor_factory=DictCursor)
        conditions = ""
        for i in range(len(values)):
            key = values.keys()[i]
            conditions += "{} = {}".format(key, values[key])
            if i != len(values):
                conditions += " AND "

        cur.execute("""SELECT * from {} where {}""".format(self.table, conditions))

    def delete(self, values: {}):
        pass
