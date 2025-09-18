from utilities.Choice import Choice
from utilities.NLP import NLP
from utilities.Avatar import Avatar
from datetime import datetime

class Demo(Avatar):

    __mainOptions = ["weather", "news", "time", "date", "exit"]

    def __init__(self):
        super().__init__(name="FakeGPT", useSR=True, vix=2)
        self.nlp = NLP()

        self.say(f"Hello, I am {self.getName()}, your virtual assistant. How can i help you today?", show=True, rate = 200)

    def getPerson(self):
        response = self.listen("Please tell me your name.", useSr=True, show=True)
        name = self.nlp.getNameByEntityType(response)
        self.say(f"Nice to meet you {name}. How can I assist you?", show=True)
        return name
        
    
    def getRequest(self):
        request = self.listen("What would you like to do?", useSr=True, show=True)
        return request

    # def sayTime(self)
    
    # def sayDate(self)
    
    # def sayWeather(self)
        
    # def sayNews(self)

    
    def run(self):
        name = ""     
        while not name:
            name = self.getPerson()
            if not name:
                self.say("I didn't catch your name. Please try again.", show=True)
        
        
        request = ""
        while request != "exit":
            request = self.getRequest()
            if not request:
                self.say("I didn't catch that. Please try again.", show=True)
            else:
                match request:
                    case "time":
                        self.sayTime()
                    case "date":
                        self.sayDate()
                    case "weather":
                        self.sayWeather()
                    case "news":
                        self.sayNews()
                    case "exit":
                        self.say("Goodbye!", show=True)
                        break
                    #case _:
                        
                        
                        

        while True:
            request = self.listen("What would you like me to do? You can ask for weather, news, time, date or say 'exit' to quit.")

def test():
    demo = Demo()
    demo.run()
if __name__ == "__main__":
    test()