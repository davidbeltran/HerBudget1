"""
Author: David Beltran
"""
import sqlite3

class Database:

    # Class constructor
    def __init__(self, statementList):
        self.statementList = statementList
        self.name = 'expenses.db'

    """
    Creates an empty SQLite table
    """
    def __createExpenseTable(self):
        try:
            conn = sqlite3.connect(self.name)
            c = conn.cursor()
            c.execute("""CREATE TABLE transactions (
                    Date text,
                    Details text,
                    Amount real
                    )""")
            conn.commit()
            conn.close()
        except sqlite3.OperationalError:
            pass

    """
    Fills SQLite table with list of expenses
    """
    def fillExpenseTable(self):
        self.__createExpenseTable()
        try:
            conn = sqlite3.connect(self.name)
            c = conn.cursor()
            rows = c.execute("""SELECT * FROM transactions""").fetchall()
            if not rows:
                c.executemany("INSERT INTO transactions VALUES (?, ?, ?)", self.statementList)
                conn.commit()
            else:
                pass
        except sqlite3.OperationalError:
            pass

