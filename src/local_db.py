import os
import logging
import sqlite3


class DbEntry:
    """Object that Represents an entry in the database"""

    def __init__(self, row):
        self.device, self.pathname, self.size = row
    
    @property
    def already_uploaded(self):
        return True

    @staticmethod
    def CreateFromSqlRow(row):
        return DbEntry(row)

class LocalDb:

    def __init__(self, config):
        self.db_conn = sqlite3.connect(config["db_path"])

    def create_table(self):
        self.db_conn.execute("CREATE TABLE photos (device text, pathname text, size int)")
        self.db_conn.commit()

    def add_new_entry(self, device, pathname, size):
        print("Adding new entry")
        t = (device, pathname, size)
        self.db_conn.execute("INSERT INTO photos VALUES (?,?,?)", t)
        self.db_conn.commit()

    def get_info(self, device, pathname, size):
        t = (pathname,)
        c = self.db_conn.cursor()
        try:
            rows = c.execute("SELECT * FROM photos WHERE pathname=?", t)
        except sqlite3.OperationalError as err:
            if str(err).startswith("no such table:"):
                self.create_table()
                rows = []
        for row in rows:
            if (row[0] == device) and (int(row[2]) == size):
#                print("Match")
                entry = DbEntry.CreateFromSqlRow(row)
                break
        else:
            self.add_new_entry(device, pathname, size)
            entry = DbEntry((device,pathname,size))

        rows = c.execute("select * from photos")
        for row in rows:
           print(row)
        return entry
