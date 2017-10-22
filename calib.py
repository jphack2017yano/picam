# -*- coding: utf-8 -*-
import cv2
import sys

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
    capture = cv2.VideoCapture(0)

    while cv2.waitKey(30) < 0 :
        _, frame = capture.read()
        frame_s = cv2.resize(frame, None, fx=0.5, fy=0.5)

        img, areas = hog_func(frame_s)
        cv2.imshow('picam', img)

    save_func(areas)
    capture.release()
    cv2.destroyAllWindows()
