from models.Database import Database
from datetime import datetime

class Result(Database):
    """Represents a single spelling attempt by a user."""
    __tableName = "results"
    __primaryKey = "resultId"
    __attributes = ["userName", "word", "attempts", "resultDate"]

    def __init__(self, userName=None, word=None, attempts=None, resultDate=None):
        super().__init__()
        self.__userName = userName
        self.__word = word
        self.__attempts = attempts
        self.__resultDate = resultDate or datetime.now().strftime("%Y-%m-%d")

    # --- Getters ---
    def getUserName(self):
        return self.__userName

    def getWord(self):
        return self.__word

    def getAttempts(self):
        return self.__attempts

    def getResultDate(self):
        return self.__resultDate

    # --- Setters ---
    def setUserName(self, userName):
        self.__userName = userName

    def setWord(self, word):
        self.__word = word

    def setAttempts(self, attempts):
        self.__attempts = attempts

    def setResultDate(self, resultDate):
        self.__resultDate = resultDate

    # --- Save to database ---
    def save(self):
        sql = f"""
            INSERT INTO {__class__.__tableName} (userName, word, attempts, resultDate)
            VALUES (?, ?, ?, ?)
        """
        params = (self.__userName, self.__word, self.__attempts, self.__resultDate)
        self.query(sql, params)

    # --- Optional: get all results for a user ---
    @staticmethod
    def loadResultsForUser(userName):
        db = Database()
        sql = f"SELECT * FROM {__class__.__tableName} WHERE userName = ? ORDER BY resultDate DESC"
        return db.query(sql, (userName,))
