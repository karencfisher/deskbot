import os
import cv2
import numpy as np

class haar_detect():
    
    def __init__(self, models):
        cwd = os.getcwd()
        self.cascades = []
        for model in models:
            path = os.path.join(cwd, model)
            cascade = cv2.CascadeClassifier(path)
            self.cascades.append(cascade)
        
    def detect(self, img):
        gsimage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        all_rects = []
        for cascade in self.cascades:
            rects = cascade.detectMultiScale(gsimage, 1.3, 5)
            for rect in rects:
                all_rects.append(rect)

        return all_rects
