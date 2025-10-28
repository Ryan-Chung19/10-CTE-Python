import sqlite3

class Database:

    __dbname = "models/Game.db"

    def __init__(self,dbname=None):
        if dbname:
            self.__dbname = dbname
        else:
            self.__dbname = Database.__dbname
    
    def query(self, sql, params=()):
        result = None

        # Normalize command check but keep original SQL for execution
        cmd = sql.strip().split()[0].lower()

        with sqlite3.connect(self.__dbname) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(sql, params)

            if cmd == "select":
                result = cur.fetchall()
            elif cmd in ("insert", "update", "delete"):
                conn.commit()
                if cmd == "insert":
                    result = cur.lastrowid
                else:
                    result = cur.rowcount  # number of rows affected
            else:
                conn.commit()
                result = None

        return result
