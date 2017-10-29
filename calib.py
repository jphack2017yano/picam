# -*- coding: utf-8 -*-
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import sys
import time

def save_func(area_arr) :
    for index, item in enumerate(area_arr) :
        name = '%04d.png' % index
        cv2.imwrite(name, item)

 
def hog_func(im):
    # HoG特徴量の計算 SVMによる人検出
    hog = cv2.HOGDescriptor()
    # hog = cv2.HOGDescriptor((32,64), (8,8), (4,4), (4,4), 9)

    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    hogParams = {'hitThreshold': 0.1, 'winStride': (4, 4), 'padding': (32, 32), 'scale': 1.05}
    # 人を検出した座標
    human, r = hog.detectMultiScale(im, **hogParams)
    human_area = []
    # 長方形で人を囲う
    for (x, y, w, h) in human:
        cv2.rectangle(im, (x, y),(x+w, y+h),(0,50,255), 3)
        human_area.append( im[y:y+h, x:x+w] )

    return im, human_area

if __name__ == '__main__':
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 16
    rawCapture = PiRGBArray(camera, size=(320, 240))

    time.sleep(2)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        image_f, areas = hog_func(image)

        cv2.imshow('picam', image_f)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            break

    save_func(areas)
    cv2.destroyAllWindows()
