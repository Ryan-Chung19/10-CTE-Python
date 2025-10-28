from utilities.Choice import Choice
from utilities.NLP import NLP
from utilities.Avatar import Avatar
from models.Word import Word
from models.Person import Person


class SpellingGame(Avatar):
    
    def __init__(self):
        # ✅ Start with speech recognition OFF
        super().__init__(name="Teacher", useSR=False, vix=2)
        self.nlp = NLP()

        self.say(f"Hello, I am your virtual {self.getName()}. Get ready to spell some words.", show=True, rate=200)

    def getPlayer(self):
        """Use speech recognition for player name only"""
        # Temporarily enable SR just for this question
        self.useSR = True
        response = self.listen("Please tell me your name.", useSr=True, show=True)
        self.useSR = False  # Disable SR for the rest of the game

        name = self.nlp.getNameByEntityType(response)
        if name:
            self.say(f"Nice to meet you, {name}.", show=True)
            return Person(userName=name, firstName=name)
        else:
            # fallback to typed input if SR fails
            typed_name = input("I didn't catch that. Please type your name: ")
            return Person(userName=typed_name, firstName=typed_name)
    
    def giveWord(self):
        """Get a random unused word from database"""
        chosenWord = Word.getRandomWord()
        if chosenWord:
            self.say(f"Spell the word: {chosenWord.getWord()}", show=True)
            return chosenWord
        else:
            self.say("You have completed all the words!", show=True)
            Word.resetWords()
            return Word.getRandomWord()

    def spellCheck(self, chosenWord):
        """Use typed input for spelling"""
        attempt = input("Please spell the word: ").strip()
        if attempt.lower() == chosenWord.getWord().lower():
            self.say("✅ Correct!", show=True)
        else:
            self.say(f"❌ Incorrect. The correct spelling is: {chosenWord.getWord()}", show=True)

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
            
            again = input("Would you like to try another word? (yes/no): ").strip().lower()
            if again not in ["yes", "y"]:
                self.say("Okay, thanks for playing! Goodbye!", show=True)
                play = False


def test():
    game = SpellingGame()
    game.run()

if __name__ == "__main__":
    test()
