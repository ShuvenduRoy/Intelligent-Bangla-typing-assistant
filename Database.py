import sqlite3 as lite
import sys


class database_handler():
    @staticmethod
    def connect():
        con = None

        try:
            con = lite.connect('test.db')

            # Test connection
            # cur = con.cursor()
            # cur.execute('SELECT SQLITE_VERSION()')
            #
            # data = cur.fetchone()
            #
            # print("SQLite version: %s" % data)
            return con

        except lite.Error as e:
            print("Error %s:" % e.args[0])
            sys.exit(1)


    @staticmethod
    def insert_sentence(string):
        con = database_handler.connect()
        with con:
            cur = con.cursor()
            cur.execute("create table if not exists history(data TEXT)")

            execution_string = "insert into history VALUES ('%s')" % string
            cur.execute(execution_string)



conn = database_handler.connect()
database_handler.insert_sentence("this is a test")