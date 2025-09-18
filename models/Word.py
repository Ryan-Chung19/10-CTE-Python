from models.Database import Database

class Word(Database):
    '''
    Attributes / Properties - Maps to Database Columns
    '''

    __word = None
    __isUsed = False

    ## Local attributes
    __tableName = "words"
    __primaryKey = "word"

    # any additional local attributes

    def __init__(self, word = None, isUsed = False):
        '''
        Contructor - Word Object
        '''

        super().__init__()
        self.setWord(word)
        self.setIsUsed(isUsed)

        if self.__exists():
            self.__getWordFromDB()

    '''
    Getters and Setters
    '''

    def getWord(self):
        return self.__word
    
    def getIsUsed(self)->bool:
        return self.__isUsed == 1
    
    def getPrimaryKey(self):
        return self.getWord()
    
    def setWord(self, word):
        self.__word = word

    def setIsUsed(self, isUsed: bool):
        self.__isUsed = 0
        if isUsed:
            self.__isUsed = 1

    '''
    Object Related Mapping Methods
    '''

    def __exists(self):
        retCode = False
        if self.getPrimaryKey():
            sql = f"SELECT EXISTS(SELECT 1 FROM {self.__tableName} WHERE {self.__primaryKey} = ?) AS row_exists"
            params = (self.getPrimaryKey(),) #comma converts it into a tuple
            result = self.query(sql, params)
            for row in result:
                if row['row_exists'] == 1:
                    retCode = True
        
        return retCode
    
    def __getWordFromDB(self):
        sql = "SELECT word, isUsed FROM words WHERE word = ?"
        params = (self.getWord(),)
        result = self.query(sql, params)

        for row in result:
            self.setWord(row['word'])
            self.setIsUsed(row['isUsed'])

    @classmethod
    def getRandomWord(cls):
        db = Database()
        sql = "SELECT * FROM words WHERE isUsed = 0 ORDER BY RANDOM() LIMIT 1"
        params = ()
        result = db.query(sql, params)
        for row in result:
            return Word(row['word'], row['isUsed'])
        else:
            return None 
        
    @classmethod
    def resetWords(cls):
        db = Database()
        sql = "UPDATE words SET isUsed = 0"
        params = ()
        db.query(sql, params)

    def save(self):
        if self.__exists():
            self.__update()
        else:
            self.__insert()

    def __insert(self):
        sql = 'INSERT INTO words (word, isUsed) VALUES (?,?)'
        params = (self.getWord(), self.__isUsed)
        self.query(sql,params)

    def __update(self):
        sql = 'UPDATE words SET isUsed = ? WHERE word = ?'
        params = (self.__isUsed, self.getWord())
        self.query(sql,params)

    '''
    Business methods
    '''

    def markAsUsed(self):
        self.setIsUsed(True)

    '''
    Utility Methods
    '''

    def __str__(self):
        return f"{self.getWord()}, {self.getIsUsed()}"
    
# TESTING
def test():
    word = Word("test", False)
    word.save()
    print(word)

    word = Word('test')
    word.markAsUsed()
    word.save()
    print(word.getWord(), word.getIsUsed())

    word = Word.getRandomWord()
    if word:
        print("Random:",word.getWord(),word.getIsUsed())
        word.markAsUsed()
        word.save()
        print("Random:",word.getWord(),word.getIsUsed())
    else:
        print("No unused random words are available please reset.")
        Word.resetWords()

if __name__ == "__main__":
    test()