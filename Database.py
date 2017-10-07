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

    @staticmethod
    def get_all_history():
        con = database_handler.connect()
        with con:
            cur = con.cursor()
            cur.execute("select * from history")
            con.commit()

            row = cur.fetchall()
            data = list(row)

        return data


    @staticmethod
    def string_strart_with(string):
        con = database_handler.connect()
        with con:
            cur = con.cursor()
            execution_string = "select data from history where data like '"+string+"%'"
            cur.execute(execution_string)
            con.commit()

            row = cur.fetchone()

        return row


# print(database_handler.string_strart_with("A"))
# print(database_handler.get_all_history())

