from rapidfuzz import fuzz
from rapidfuzz import process, utils

class Choice:

    @staticmethod
    def getChoice(query, options, minConfidence=70):

        (choice, confidence, index) = process.extractOne(query, options, scorer = fuzz.partial_token_set_ratio, processor=utils.default_process)

        print(f"Found '{choice}' with confidence {confidence} and index {index}")

        if confidence > minConfidence:
            return choice
        else:
            return None
        
    @staticmethod
    def getChoices(query, options, minConfidence=70):

        choices = []
        results = process.extract(query, options, scorer = fuzz.partial_ratio, processor = utils.default_process)

        for (choice, confidence, index) in results:
            print(f"Found '{choice}' with confidence {confidence} and index {index}")

            if confidence > minConfidence:
                choices.append(choice)
        
        return choices 

# query = "I am going to say Yes please"
# choices = ["Yes", "No"]

# choice = Choice.getChoice(query, choices)
# print(choice)

# query = "Steak"
# choices = ["Steak", "Soup", "Ice cream", "Fish and Chips", "Pizza", "Pasta"]
# choices = Choice.getChoice(query, choices)
# for choice in choices:
#     print(f"Choice: {choice}")