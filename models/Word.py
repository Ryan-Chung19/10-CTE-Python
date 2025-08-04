from Database import Database

class Word(Database):
    '''
    Attributes / Properties - Maps to Database Columns
    '''

    __word = None
    __isUsed = False

    def __init__(self, word = None, isUsed = False):
        '''
        Contructor - Word Object
        '''

        super().__init__()
        self.setWord(word)
        self.setIsUsed(isUsed)

        if self.exists():
            self.getWordFromDB()

    '''
    Getters and Setters
    '''

    def getWord(self):
        return self.__word
    
    def getIsUsed(self)->bool:
        return self.__isUsed == 1
    
    def setWord(self, word):
        self.__word = word

    def setIsUsed(self, isUsed: bool):
        self.__isUsed = 0
        if isUsed:
            self.__isUsed = 1

    '''
    Object Related Mapping Methods
    '''

    def exists(self):
        retCode = False
        if self.getWord():
            sql = "SELECT EXISTS(SELECT 1 FROM words WHERE word = ?) AS row_exists"
            params = (self.getWord(),) #comma converts it into a tuple
            result = self.query(sql, params)
            for row in result:
                if row['row_exists'] == 1:
                    retCode = True
        
        return retCode
    
    def getWordFromDB(self):
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

    def save(self):
        if self.exists():
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

def test():
    word = Word("test", False)
    word.save()
    print(word.getWord(),word.getIsUsed())

    word = Word('test')
    word.markAsUsed()
    word.save()
    print(word.getWord(), word.getIsUsed())

    word = Word.getRandomWord()
    word.markAsUsed()
    word.save()
    print("Random:",word.getWord(),word.getIsUsed())

if __name__ == "__main__":
    test()