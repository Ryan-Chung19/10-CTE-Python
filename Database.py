import sqlite3

class Database:
    __dbname = None
    __conn = None

    def __init__(self,dbname):
        self.setDbname(dbname)
        self.setConn()

    def setDbname(self,dbname):
        self.__dbname=dbname

    def getDbname(self):
        return self.__dbname
    
    def setConn(self):
        self.__conn = sqlite3.connect(self.__dbname)