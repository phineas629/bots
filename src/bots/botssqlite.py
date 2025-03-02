# -*- coding: utf-8 -*-


import re
import sqlite3
import sys

# Fix regex pattern with proper escaping for Python 3
reformatparamstyle = re.compile(r"%\((?P<n>[^)]+)\)s")

sqlite3.register_adapter(bool, int)  # python type -> SQL type
sqlite3.register_converter(str("BOOLEAN"), lambda s: bool(int(s)))  # SQL type -> python type


def connect(database):
    con = sqlite3.connect(
        database,
        factory=BotsConnection,
        detect_types=sqlite3.PARSE_DECLTYPES,
        timeout=99.0,
        isolation_level="EXCLUSIVE",
    )
    con.row_factory = sqlite3.Row
    con.execute("""PRAGMA synchronous=OFF""")
    return con


class BotsConnection(sqlite3.Connection):

    def cursor(self):
        return sqlite3.Connection.cursor(self, factory=BotsCursor)


class BotsCursor(sqlite3.Cursor):
    """
    bots engine uses:
        SELECT * FROM ta WHERE idta=%(idta)s,{'idta':12345})
    SQLite wants:
        SELECT * FROM ta WHERE idta=:idta ,{'idta': 12345}
    """

    def execute(self, string, parameters=None):
        if parameters is None:
            sqlite3.Cursor.execute(self, string)
        else:
            sqlite3.Cursor.execute(self, reformatparamstyle.sub(r":\g<n>", string), parameters)
