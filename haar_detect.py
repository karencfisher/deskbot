import cv2
import numpy as np

class haar_detect():
    
    def __init__(self, models):
        path = '/home/pi/.local/lib/python3.5/site-packages/cv2/data/'
        self.cascades = []
        for model in models:
            cascade = cv2.CascadeClassifier(path + model)
            self.cascades.append(cascade)
        
    def detect(self, img):
        gsimage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        all_rects = []
        for cascade in self.cascades:
            rects = cascade.detectMultiScale(gsimage, 1.3, 5)
            for rect in rects:
                all_rects.append(rect)

        return all_rects
