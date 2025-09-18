from rapidfuzz import fuzz
from rapidfuzz import process, utils

spellOptions = ["Spell", "Spelling", "Spell Check", "Spell Checker"]
summaryOptions = ["Summary", "Summarize", "Summarization"]
exitOptions = ["Exit", "Quit", "Leave", "Bye"]

choices = spellOptions + summaryOptions + exitOptions

query = "I want to Spell some words please"

print(f"Check '{query}' in {choices}")

(choice, confidence, index) = process.extractOne(query, choices, scorer = fuzz.WRatio, processor=utils.default_process)

print(f"extractOne Found '{choice}' with {confidence} and index of {index}")

match choice:
    case choice if choice in spellOptions:
        print(f"Spell Check Selected: {choice}")
    
    case choice if choice in summaryOptions:
        print(f"Spell Check Selected: {choice}")
    
    case choice if choice in exitOptions:
        print(f"Spell Check Selected: {choice}")

print(f"\nNow checking all matches for '{query}' in {choices}: \n")
results = process.extract(query, choices, scorer=fuzz.WRatio, processor=utils.default_process)

for result in results:
    print(f"Found '{result[0]}' with confidence {result[1]} and distance {result[2]}")

