import pyttsx4
import speech_recognition as sr

class Avatar():
    '''
    Avatar class is responsible for speaking and listening.
    '''

    def __init__(self, name = None, useSR = True, vix = 3):
        '''
        Constructor
        '''
        # if name:
        #     self.__name = name 
        self.__name = name if name else "Avatar"

        self.__useSR = useSR
        self.__initVoice(vix)
        self.__initSR()
        

    def __initVoice(self, vix = 3):
        '''
        Method: Initialise text to speech
        '''
        self.__engine = pyttsx4.init()
        self.__voices = self.__engine.getProperty('voices')
        self.__vix = vix
        self.__rate = 200
        self.__voice = self.__voices[self.__vix].id
        self.__engine.setProperty('voice', self.__voice)
        self.__engine.setProperty('rate', self.__rate)
        self.__engine.setProperty('volume', 1.0)

    def __initSR(self, useSr = True):
        self.sample_rate = 48000
        self.chunck_size = 2048
        self.r = sr.Recognizer()
        if useSr is not None:
            self.__useSR = useSr
        else:
            self.__useSR = True

    def say(self, words, show = True, rate = None):
        '''
        Method: Speak the words
        '''
        if show:
            print(f"{words}")

        if rate:
            self.__engine.setProperty('rate', rate)
        self.__engine.say(words, self.__name)
        self.__engine.runAndWait()

        self.__engine.setProperty('rate', self.__rate)

    def listen(self, prompt = None, useSr = None, show = True):
        if useSr is not None:
            self.__useSR = useSr
        
        words = ""
        if self.__useSR:
            try:
                with sr.Microphone(sample_rate=self.sample_rate, chunk_size=self.chunck_size) as (source):
                    self.r.adjust_for_ambient_noise(source)
                    self.say(prompt, show)
                    audio = self.r.listen(source, timeout = 5, phrase_time_limit= 3)
                    with open("audio.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                try:
                    print("Ok. Trying to understand what you just said... please wait.")
                    # words = self.r.recognize_google(audio, language = "en-US")
                    words = self.r.recognize_whisper(audio, language="english")
            
                except sr.UnknownValueError:
                    self.say("Could not understand what you said.", show)
                except sr.RequestError as e:
                    self.say(f"Could not request results: {e}", show)
        
            except Exception as e:
                print(f"Error listening: '{e}'. ")
                self.say(prompt, show)
                words = input("Please type your responses: ")
        
        else:
            self.say(prompt, show = True)
            words = input(">") 

        return words        
            

    def getName(self):
        return self.__name

def main():
    george = Avatar("")
    # george.say(f"Give me {george.getName()}", rate = 150)

    # response = george.listen("Please tell me what you want to do.", useSr = True, show = True)
    # george.say(f"You said: {response}", show = True, rate = 200)

main()
