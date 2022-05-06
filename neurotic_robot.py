import talker
import listener
import face_track as ft
from multiprocessing import Process, Lock, Queue, Value
import cv2
import os


def listening(lock, listen, talk, q):
    
    print("Begin process:", os.getpid())
    lock.acquire()
    talk.talk("I am listening")
    lock.release()
    
    while True:  
        text = listen.listen()
        if text == '':
            continue
        elif text == 'goodbye' or text == 'bye':
            q.put('text')
            break
        
        lock.acquire()
        talk.talk(text)
        lock.release()
        
    print('Exiting process:', os.getpid())



def main():
    listening_flag = False
    listeninig_process = None
    
    #initialize speech synthesis 
    talk = talker.talker()
    spoke = False
    
    #initialize speech recognition
    listen = listener.listener()
    
    #and face tracking
    watch = ft.facetrack()
    
    #initialize lock for audio output
    speaker_lock = Lock()
    output_queue = Queue()
    
    talk.talk("I am ready")
    print("Main process:", os.getpid())

    os.environ['DISPLAY'] = ':0'
    
    while True:
        
        #get visual and track
        distance, face_rects, image = watch.update()
        
        #display marked up image
        cv2.imshow('camera', image)
        key = cv2.waitKey(1)
        if key > 0:
            listening_process.terminate()
            break
        
        #depending on if you are looking at her
        if distance == 0:
            
            speaker_lock.acquire()
            talk.talk("Where did you go?")
            speaker_lock.release()
            spoke = False
                
        else:
            if not spoke:
                speaker_lock.acquire()
                talk.talk("I see you.")
                speaker_lock.release()
                spoke = True
            
            if not listening_flag:
                listening_process = Process(target=listening, args=(speaker_lock,
                                                listen, talk, output_queue))
                listening_process.start()
                listening_flag = True
            
        if not output_queue.empty():
            break
            
            
    #cleanup
    #if speech recognition is running, flag it to stop and wait
    if listening_flag:
        listening_process.join()
    
    #close seeing
    cv2.destroyAllWindows()
    watch.cleanup()
    
    #and cease speech synthesis
    talk.talk("See you later")
    talk.cleanup()
    print("Exiting")
    
    raise SystemExit()
    
if __name__ == '__main__':
    main()
