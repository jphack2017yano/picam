# -*- coding: utf-8 -*-
import cv2
import sys

def compare_hist_func(im, area_arr) :
    for item in area_arr :
        hist = cv2.calcHist([item], [0], None, [256], [0,256])

 
def hog_func(im):
    # HoG特徴量の計算 SVMによる人検出
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    hogParams = {'winStride': (8, 8), 'padding': (32, 32), 'scale': 1.05}
    # 人を検出した座標
    human, r = hog.detectMultiScale(im, **hogParams)
    human_area = []
    # 長方形で人を囲う
    for (x, y, w, h) in human:
        # cv2.rectangle(im, (x, y),(x+w, y+h),(0,50,255), 3)
        human_area.append( im[y:y+h, x:x+w] )

    compare_hist_func(im, human_area)
    # 人を検出した座標
    return im

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)

    while cv2.waitKey(30) < 0 :
        _, frame = capture.read()
        frame_s = cv2.resize(frame, None, fx=0.5, fy=0.5)

        img = hog_func(frame_s)
        cv2.imshow('picam', img)

    capture.release()
    cv2.destroyAllWindows()
