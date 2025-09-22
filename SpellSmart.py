from utilities.Choice import Choice
from utilities.NLP import NLP
from utilities.Avatar import Avatar
from models.Word import Word
from models.Person import Person
import random

class SpellingGame(Avatar):
    
    def __init__(self):
        super().__init__(name="Teacher", useSR=True, vix = 2)
        self.nlp = NLP()

        # this line for adding the database

        self.say(f"Hello, I am your virtual {self.getName()}. Get ready to spell some words.", show = True, rate =200)

    def getPlayer(self):
        response = self.listen("Please tell me your name.", useSr=True, show=True)
        name = self.nlp.getNameByEntityType(response)
        if name:
            self.say(f"Nice to meet you, {name}.", show=True)
            player = Person(userName=name, firstName=name)
            return player
        return None
    
    def giveWord(self):
        '''Get a random unused word from database'''
        chosenWord = Word.getRandomWord()
        if chosenWord:
            self.say(f"Spell the word {chosenWord.getWord()}", show=True)
        else:
            self.say("You have completed all the words!", show=True)
        #     Word.resetWords()
        #     chosenWord = Word.getRandomWord()
        #     if chosenWord:
        #         self.say(f"Spell the word {chosenWord.getWord()}", show=True)
        # return chosenWord

    def spellCheck(self, chosenWord):
        attempt = self.listen(f"Please spell the word.", useSr=True, show=True)
        if attempt.lower().strip() == chosenWord.getWord().lower():
            self.say(f"Correct!", show = True)
        else:
            self.say(f"Incorrect. The correct spelling is: {chosenWord.getWord()}", show=True)
        chosenWord.markAsUsed()
        chosenWord.save()

    def run(self):
        player = None
        while not player:
            player = self.getPlayer()
            if not player:
                self.say("I didn't catch your name. Please try again.", show=True)
        
        play = True
        while play:
            chosenWord = self.giveWord()
            if chosenWord:
                self.spellCheck(chosenWord)
            
            again = self.listen("Would you like to try another word? Say yes or no.", useSr=True, show=True)
            if again.lower() not in ["yes", "y"]:
                self.say("Okay, thanks for playing! Goodbye!", show=True)
                play = False

def test():
        game = SpellingGame()
        game.run()

if __name__ == "__main__":
    test()