import talker
import listener
import face_track
from multiprocessing import Process, Lock, Value
import cv2
import os


class Bot:
    def __init__(self):
        #initialize speech synthesis 
        self.__talk = talker.talker()
        self.__spoke = False
        
        #initialize speech recognition
        self.__listen = listener.listener()
        
        #and face tracking
        self.__watch = face_track.facetrack()

    def listening(self, listening_flag):  
        print("Begin process:", os.getpid())
        self.__talk.talk("I am listening")
        
        while listening_flag:  
            text = self.__listen.listen()
            if text == '':
                continue
            elif text == 'goodbye' or text == 'bye':
                listening_flag = False
            self.__talk.talk(text)
        print('Exiting process:', os.getpid())

    def run(self):
        print("Main process:", os.getpid())
        listening_flag = Value(bool, True)
        listening_process = Process(target=self.listening, args=(listening_flag,))
        listening_process.start()
        while True:
            #get visual and track
            distance, _, image = self.__watch.update()
            
            #display marked up image
            cv2.imshow('camera', image)
            key = cv2.waitKey(1)
            if key > 0:
                break
            
            #depending on if you are looking at her
            if distance == 0:
                self.__talk.talk("Where did you go?")
                spoke = False
                    
            else:
                if not self.__spoke:
                    self.__talk.talk("I see you.")
                    self.__spoke = True
                
            if not listening_flag:
                break
                
        #cleanup
        #if speech recognition is running, flag it to stop and wait
        listening_process.join()
        
        #close seeing
        cv2.destroyAllWindows()
        self.__watch.cleanup()
    
        #and cease speech synthesis
        self.__talk.cleanup()
        print("Exiting")
        
        raise SystemExit()
    
if __name__ == '__main__':
    bot = Bot()
    bot.run()
