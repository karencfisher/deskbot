import talker
import listener
import face_track
from multiprocessing import Process, Lock, Value
from ctypes import c_bool
import cv2
import os


class Bot:
    def __init__(self):
        #initialize speech synthesis 
        self.talk = talker.talker()
        self.spoke = False
        
        #initialize speech recognition
        self.listen = listener.listener()
        
        #and face tracking
        self.watch = face_track.facetrack()

    def listening(self, listening_flag):  
        print("Begin process:", os.getpid())
        self.talk.talk("I am listening")
        
        while listening_flag.value:  
            text = self.listen.listen()
            if text == '':
                continue
            elif text == 'goodbye' or text == 'bye':
                listening_flag.value = False
            self.talk.talk(text)
        print('Exiting process:', os.getpid())

    def watching(self, listening_flag):
        os.environ['DISPLAY'] = ':0'
        while listening_flag.value:
            #get visual and track
            distance, _, image = self.watch.update()
            
            #display marked up image
            cv2.imshow('camera', image)
            key = cv2.waitKey(1)
            if key > 0:
                break
            
            #depending on if you are looking at her
            if distance == 0:
                self.talk.talk("Where did you go?")
                self.spoke = False
                    
            else:
                if not self.spoke:
                    self.talk.talk("I see you.")
                    self.spoke = True

    def run(self):
        print("Main process:", os.getpid())
        listening_flag = Value(c_bool, True)
        listening_process = Process(target=self.listening, args=(listening_flag,))
        listening_process.start()

        # Run the watching loop (This process)
        self.watching(listening_flag)
                
        #cleanup
        #if speech recognition is running, flag it to stop and wait
        listening_process.join()
        
        #close seeing
        cv2.destroyAllWindows()
        self.watch.cleanup()
    
        #and cease speech synthesis
        self.talk.cleanup()
        print("Exiting")
        
        raise SystemExit()
    
if __name__ == '__main__':
    bot = Bot()
    bot.run()
