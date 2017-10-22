# -*- coding: utf-8 -*-
import io
import cv2
import sys
import time
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

x_arr = ['OK', 'OK', 'OK']
y_arr = ['OK', 'OK', 'OK']

def compare_hist_func(area_arr) :
    model_im = cv2.imread('0001.png')
    model = cv2.calcHist([model_im], [0], None, [256], [0,256])

    rel_max = 0.0
    rel_max_ind = None
    for index, item in enumerate( area_arr ) :
        hist = cv2.calcHist([item['img']], [0], None, [256], [0,256])
        rel = cv2.compareHist(hist, model, 0)
        if (rel > rel_max) :
            rel_max = rel
            rel_max_ind = index

    return rel_max_ind

def lr_func(im, x, y) :
    center_x = int( im.shape[1]/2 )
    center_y = int( im.shape[0]/2 )
    area = 100

    if x < center_x-area:
        x_axis = 'L'
    elif x > center_x+area:
        x_axis = 'R'
    else :
        x_axis = 'OK'

    if y < center_y-area:
        y_axis = 'U'
    elif y > center_y+area :
        y_axis = 'D'
    else :
        y_axis = 'OK'

    return x_axis, y_axis

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
        human_area.append( {'img': im[y:y+h, x:x+w], 'x': x, 'y': y} )

    rel_max_ind = compare_hist_func(human_area)
    if rel_max_ind != None :
        cv2.circle( im, ( human_area[rel_max_ind]['x'] + int(human_area[rel_max_ind]['img'].shape[1]/2), human_area[rel_max_ind]['y'] + int(human_area[rel_max_ind]['img'].shape[0]/2)), 5, (255, 50, 0), 3)
        x_axis, y_axis = lr_func( im, human_area[rel_max_ind]['x'] + int(human_area[rel_max_ind]['img'].shape[1]/2), human_area[rel_max_ind]['y'] + int(human_area[rel_max_ind]['img'].shape[0]/2))

        x_arr.append(x_axis)
        del x_arr[0]
        y_arr.append(y_axis)
        del y_arr[0]

        if len(list(filter(lambda item:item == x_arr[0], x_arr))) == 3 :
            print 'x'
# 左右の方向転換
        if len(list(filter(lambda item:item == y_arr[0], y_arr))) == 3 :
            print 'y'
# 上下の方向転換

    # 人を検出した座標
    return im

if __name__ == '__main__':
    stream = io.BytesIO()
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    camera.capture(stream, format='jpeg')
    rawCapture = PiRGBArray(camera, size=(640, 480))

    time.sleep(0.1)

    for frames in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # while cv2.waitKey(30) < 0 :
        # _, frame = capture.read()
        frame = frames.array
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        frame = cv2.imdecode(data, 1)
        frame_s = cv2.resize(frame, None, fx=0.5, fy=0.5)
        img = hog_func(frame_s)
        cv2.imshow('picam', img)

    capture.release()
    cv2.destroyAllWindows()
