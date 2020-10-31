import cv2
import numpy as np
import picamera, picamera.array
import time
import haar_detect
import talker 
from adafruit_servokit import ServoKit
import pid

# define pan function
prev_x = 0
prev_y = 0

class facetrack():
    
    def __init__(self):
        
        # set constants
        self.screenWidth = 320
        self.screenHeight = 240
        self.F = 300 # aproximately
        
        # initialize PID controllers
        self.pidc_x = pid.PID(0.01, 0.07, 0.0001)
        self.pidc_y = pid.PID(0.05, 0.07, 0.0001)
        
        # and servo controller
        self.servo = ServoKit(channels=16)
        self.__center()

        # initialize detection
        models = ['haarcascade_frontalface_default.xml']
        self.detector = haar_detect.haar_detect(models)
        
        #set up camera, pause for warmup
        self.camera = picamera.PiCamera()
        self.camera.resolution = (self.screenWidth, self.screenHeight)
        time.sleep(1)
    
    
    def __within(self, current, previous, margin=0.1):
        diff = abs(previous * margin)
            
        min = previous - diff
        max = previous + diff
        
        if current >= min and current <= max:    
            result = True
        else:
            result = False
            
        return result


    def __between(self, value, min, max):
        if value <= min or value >= max:
            result = False
        else:
            result = True
            
        return result


    def __center(self):
        global prev_x, prev_y
        self.servo.servo[0].angle=90
        self.servo.servo[1].angle=178
        self.pidc_x.initialize()
        self.pidc_y.initialize()


    def __pan_camera(self, faceRects):
        # center of face in image
        
        #if no data (no face detection), exit function
        if len(faceRects) == 0:
            self.__center()
            return 0.
        
        # Calculate ratio of image height and ROI height
        height = faceRects[0][3]
        width = faceRects[0][2]
     
        #calculate distance to subject
        distance = (self.F * 14)/width
        
        # calculate the center of the ROI and from that the offset from the center of the image
        center_x = self.screenWidth // 2
        center_y = self.screenHeight // 2
        x = faceRects[0][0] + (width // 2)
        y = faceRects[0][1] + (height // 2)
        
        if not self.__within(x, center_x, margin=.05):
            error = self.screenWidth // 2 - x 
            xd = self.pidc_x.update(error, 0.2)
            angle = np.rad2deg(np.arctan(distance / abs(xd)))
            if xd < 0:
                angle_x = angle
            else:
                angle_x = 180 - angle  
                
            if self.__between(angle_x, 10, 170):
                self.servo.servo[0].angle = angle_x
                time.sleep(.2)
                           
        if not self.__within(y, center_y, margin=.05):
            error = self.screenHeight // 2 - y
            yd = self.pidc_y.update(error, 0.2)
            angle_y = 130 + np.rad2deg(np.arctan(distance / yd))
            
            if self.__between(angle_y, 150, 180):
                self.servo.servo[1].angle = angle_y
                time.sleep(.2)
    
        return round(distance, 2)
    
    
    def update(self):    
        #capture image as CV image
        stream = picamera.array.PiRGBArray(self.camera)
        self.camera.capture(stream, format='bgr')
        image = stream.array
        
        #run face detection
        face_rects = self.detector.detect(image)
        
        #pan camera
        d = self.__pan_camera(face_rects)
        
        #update image
        for (x, y, w, h) in face_rects:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 3)
        
        return d, face_rects, image
    
    
    def cleanup(self):
        self.__center()
    
    

#test code
if __name__ == '__main__':
    
    track = facetrack()
    talk = talker.talker()
    spoke = False
    
    # start
    talk.talk("I am ready")
    
    while True:
        distance, face_rects, image = track.update()
        
        #display marked up image
        cv2.imshow('camera', image)
        key = cv2.waitKey(1)
        if key > 0:
            break
        
        if distance == 0:
            talk.talk("Where did you go?")
            spoke = False
        elif not spoke:
            talk.talk("I see you.")
            spoke = True
    
    #clean up
    cv2.destroyAllWindows()
    track.cleanup()

    talk.talk("Goodbye")
    talk.cleanup()
    raise SystemExit()

