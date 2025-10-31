from utilities.Choice import Choice
from utilities.NLP import NLP
from utilities.Avatar import Avatar
from models.Word import Word
from models.Person import Person
from rapidfuzz import fuzz
from models.Result import Result


class SpellingGame(Avatar):
    
    def __init__(self):
        super().__init__(name="Teacher", useSR=False, vix=2)
        self.nlp = NLP()

        self.say(f"Hello, I am your virtual {self.getName()}. Get ready to spell some words.", show=True, rate=200)

    def getPlayer(self):
        """Use speech recognition for player name only"""
        while True:
            self.say("Would you like to create a new user, or use an existing one?", show=True)

            choice = input("Type 'New' to create a new user or 'existing' to use an existing one: ")

            # NEW USER PART
            if choice in ["new", "n", "create", "c"]:
                while True:

                    self.useSR = True
                    first_name_response = self.listen("Please tell me your first name.", useSr=True, show=True)
                    self.useSR = False  # Disable SR for the rest of the game
                    first_name = self.nlp.getNameByEntityType(first_name_response)

                    if not first_name:
                        self.say("I didn't catch that, please say your first name again.", show=True)
                        continue

                    self.useSR = True
                    last_name_response = self.listen("Please tell me your last name.",useSr=True, show=True)
                    self.useSR = False
                    last_name = self.nlp.getNameByEntityType(last_name_response)
                    
                    if not last_name:
                        self.say("I didn't catch that. Please say your last name again.", show=True)
                        continue

                    self.say("Now please type your user name.", show=True)
                    username = input("Username: ").strip()

                    if not username:
                        self.say("Username cannot be empty. Please try again.", show=True)
                        continue

                    existing_player = Person(userName=username)
                    if existing_player.getFirstName() is not None:
                        self.say("That user name already exists. Please choose another one.", show=True)
                        continue
                    else:
                        break
                    

                player = Person(userName=username, firstName = first_name, lastName = last_name)
                player.save()
                
                self.say(f"Details saved successfully. Welcome {first_name}.")

                return player
            
            elif choice in ["existing", "exist", "old", "e"]:
                while True:
                    self.say("Please type your existing user name.")
                    username = input("Username: ").strip()

                    if not username:
                        self.say("User name cannot be empty. Please try again.", show=True)
                        continue

                    player = Person(userName=username)
                    if player.getFirstName() is None:
                        self.say("No user found with that user name. Please try again or create a new one.", show = True)
                        continue
                    else:
                        self.say(f"Welcome back {player.getFirstName()}!", show=True)
            else:
                self.say("I didn't understand that. Please type 'new' or 'existing'.", show=True)


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

    def spellCheck(self, chosenWord, player=None):
        """Check spelling accuracy, repeat until correct, save results, and return stats."""
        correct_word = chosenWord.getWord().lower()
        attempts = 0

        while True:
            attempt = input("Please spell the word: ").strip().lower()
            attempts += 1
            accuracy = fuzz.ratio(attempt, correct_word)

            if accuracy == 100:
                self.say("Correct! Perfect spelling!", show=True)
                chosenWord.markAsUsed()
                chosenWord.save()

                if player is not None:
                    result = Result(
                        userName=player.getUserName(),
                        word=chosenWord.getWord(),
                        attempts=attempts
                    )
                    result.save()

                return {
                    "word": chosenWord.getWord(),
                    "accuracy": 100,
                    "attempts": attempts
                }

            else:
                self.say(f"Incorrect. Accuracy: {accuracy:.1f}%", show=True)
                self.say(f"Let's try again. Spell the word '{correct_word}'.", show=True)

    # Display of results
    def displayResultsSummary(self, results):
        """Display a summary of the user's spelling session."""
        if not results:
            self.say("No results to show. Maybe next time!", show=True)
            return

        total_words = len(results)
        correct_words = sum(1 for r in results if r["accuracy"] == 100)

        self.say(f"\n Congratulations! You got {correct_words} out of {total_words} words correct!\n", show=True)

        for r in results:
            self.say(f"{r['word']}  {r['accuracy']}%  Attempts: {r['attempts']}", show=True)



    def run(self):
        player = None
        while not player:
            player = self.getPlayer()
            if not player:
                self.say("I didn't catch your name. Please try again.", show=True)

        session_results = []  

        play = True
        while play:
            chosenWord = self.giveWord()

            if not chosenWord:
                self.say("You have completed all the words!", show=True)
                break

            result_info = self.spellCheck(chosenWord, player)
            session_results.append(result_info)

            again = input("Would you like to try another word? (yes/no): ").strip().lower()
            if again not in ["yes", "y"]:
                self.say("Okay, thanks for playing! Goodbye!", show=True)
                play = False

        self.displayResultsSummary(session_results)
        Word.resetWords()



def test():
    game = SpellingGame()
    game.run()

if __name__ == "__main__":
    test()
