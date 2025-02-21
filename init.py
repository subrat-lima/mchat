import os
import sqlite3

from mchat.helper import db_connect


@db_connect
def init_db(curs):
    with open("mchat/schema.sql") as f:
        query = f.read()
        curs.executescript(query)


def main():
    directory = "instance"
    os.makedirs(directory, exist_ok=True)
    init_db()
    print("database initialized")


if __name__ == "__main__":
    main()
