import sqlite3

class Database:
    __dbname = "Game.db"

    def __init__(self,dbname="Game.db"):
        if dbname:
            self.__dbname = dbname
    
    def query(self, sql, params=()):
        result = None

        with sqlite3.connect(self.__dbname) as conn:
            sql = sql.strip().lower()
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(sql, params)

            isSelect = sql.startswith("select")
            isInsert = sql.startswith("insert")

            if isSelect:
                result = cur.fetchall()
            elif isInsert:
                conn.commit()
                result = cur.lastrowid
            else:
                conn.commit()
                result = None
    
        return result