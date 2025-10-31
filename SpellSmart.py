from utilities.Choice import Choice
from utilities.NLP import NLP
from utilities.Avatar import Avatar
from models.Word import Word
from models.Person import Person
from rapidfuzz import fuzz


class SpellingGame(Avatar):
    
    def __init__(self):
        # ✅ Start with speech recognition OFF
        super().__init__(name="Teacher", useSR=False, vix=2)
        self.nlp = NLP()

        self.say(f"Hello, I am your virtual {self.getName()}. Get ready to spell some words.", show=True, rate=200)

    def getPlayer(self):
        """Use speech recognition for player name only"""
        # Temporarily enable SR just for this question
        while True:
            self.useSR = True
            response = self.listen("Please tell me your name.", useSr=True, show=True)
            self.useSR = False  # Disable SR for the rest of the game

            name = self.nlp.getNameByEntityType(response)
            
            if name:
                self.say(f"Nice to meet you, {name}.", show=True)
                return Person(userName=name, firstName=name)
            else:
                self.say("I didn't catch that. Please say your name again.", show=True)
                
    
    def giveWord(self):
        """Get a random unused word from database"""
        chosenWord = Word.getRandomWord()
        if chosenWord:
            self.say(f"Spell the word: {chosenWord.getWord()}", show=True)
            return chosenWord
        else:
            self.say("You have completed all the words!", show=True)
            self.say(f"That was some good practice.")
            Word.resetWords()
            return None

    def spellCheck(self, chosenWord):
        correct_word = chosenWord.getWord().lower()
        while True:
            attempt = input("Please spell the word: ").strip()
            accuracy = fuzz.ratio(attempt, correct_word)

            if accuracy == 100:
                self.say("Correct! Perfect spelling.", show=True)
                chosenWord.markAsUsed()
                chosenWord.save()
                break
            else:
                self.say(f"Incorrect. Accuracy: {accuracy:.1f}%", show=True)
                self.say(f"Let's try again. Spell the word {correct_word} again.", show=True)

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
            if not chosenWord:
                self.say("Okay, thanks for playing! Goodbye!", show=True)
                break
                
            self.spellCheck(chosenWord)
            
            again = input("Would you like to try another word? (yes/no): ").strip().lower()
            if again not in ["yes", "y"]:
                self.say("Okay, thanks for playing! Goodbye!", show=True)
                play = False


def test():
    game = SpellingGame()
    game.run()

if __name__ == "__main__":
    test()
