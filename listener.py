import speech_recognition as sr
import talker
import time
    
class listener():
    
    def __init__(self):
        
        self.recog = sr.Recognizer()
        self.mic = sr.Microphone()
        self.recog.energy_threshold = 650
        self.recog.dynamic_energy_threshold = False
        
    def __process_audio(self, audio):
        print('processing')
        text = ''
        try:
            text = self.recog.recognize_google(audio)
            print(text)
      
        except sr.UnknownValueError: 
            text = "Sorry, I did not understand" 
              
        except sr.RequestError as e: 
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        return text
     
    def listen(self):
        with self.mic as source:
            print('ready...')
            audio = self.recog.listen(source, phrase_time_limit=2)
            
        return self.__process_audio(audio)


#test code
if __name__ == '__main__':
    
    talk = talker.talker()
    l = listener()
    
    talk.talk("I am listening")
    while True:
        
        text = l.listen()
        if text == '':
            continue
        elif text == 'goodbye' or text == 'bye':
            break
        
        talk.talk(text)
         
    
    talk.talk("See you later")
    talk.cleanup()
    
    
        
    
    