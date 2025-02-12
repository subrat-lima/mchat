import sqlite3


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def db_connect(func):
    def _db_connect(*args, **kwargs):
        conn = sqlite3.connect("mchat.db")
        conn.row_factory = dict_factory
        curs = conn.cursor()
        result = func(curs, *args, **kwargs)
        conn.commit()
        conn.close()
        return result

    return _db_connect


@db_connect
def db_init(curs):
    with open("mchat/model/schema.sql") as f:
        query = f.read()
    curs.executescript(query)


db_init()
