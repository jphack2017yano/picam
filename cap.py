# -*- coding: utf-8 -*-
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import sys
import time
import serial
import requests

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
    x_area = 50
    y_area = 30

    if x < center_x-x_area:
        x_axis = 'R'
    elif x > center_x+x_area:
        x_axis = 'L'
    else :
        x_axis = 'OK'

    if y < center_y-y_area:
        y_axis = 'U'
    elif y > center_y+y_area :
        y_axis = 'D'
    else :
        y_axis = 'OK'

    return x_axis, y_axis

def hog_func(im, capcount):
    # HoG特徴量の計算 SVMによる人検出
    s = serial.Serial("/dev/ttyS0",9600,timeout=10)
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
        # cv2.circle( im, ( human_area[rel_max_ind]['x'] + int(human_area[rel_max_ind]['img'].shape[1]/2), human_area[rel_max_ind]['y'] + int(human_area[rel_max_ind]['img'].shape[0]/2)), 5, (255, 50, 0), 3)
        cv2.rectangle(im, ( human_area[rel_max_ind]['x'], human_area[rel_max_ind]['y'] ), ( human_area[rel_max_ind]['img'].shape[1], human_area[rel_max_ind]['img'].shape[0] ), (255, 10, 0), 3)
        x_axis, y_axis = lr_func( im, human_area[rel_max_ind]['x'] + int(human_area[rel_max_ind]['img'].shape[1]/2), human_area[rel_max_ind]['y'] + int(human_area[rel_max_ind]['img'].shape[0]/2))


        x_arr.append(x_axis)
        del x_arr[0]
        y_arr.append(y_axis)
        del y_arr[0]

        x_flag = False
        y_flag = False

        print('x : ', x_arr)
        print('y : ', y_arr)
        if len(list(filter(lambda item:item == x_arr[0], x_arr))) == 6 :
            if x_arr[0] == 'OK' :
                x_flag = True
            elif x_arr[0] == 'L' :
                s.write('l')
            elif x_arr[0] == 'R' :
                s.write('r')
        if len(list(filter(lambda item:item == y_arr[0], y_arr))) == 6 :
            if y_arr[0] == 'OK' :
                y_flag = True
            elif y_arr[0] == 'U' :
                s.write('u')
            elif y_arr[0] == 'D' :
                s.write('d')

        if (x_flag and y_flag) :
            capcount += 1
        else :
            capcount = 0

    # 人を検出した座標
    return im, capcount

def sendImage(im) :
    cv2.imwrite('out.png', im)
    url = 'http://ec2-18-216-61-164.us-east-2.compute.amazonaws.com/image/upload?id=nurunuru'
    files = {'image':open('out.png', 'rb')}
    r = requests.post(url, files=files)

if __name__ == '__main__':
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 16
    rawCapture = PiRGBArray(camera, size=(320, 240))

    capcount = 0
    capnum = 1
    time.sleep(2)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        image_f, capcount = hog_func(image, capcount)
        cv2.imshow("Frame", image_f)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if capcount == 3 :
            sendImage(image)
        if key == ord("c"):
            sendImage(image)
        elif key == ord("q"):
            break

    cv2.destroyAllWindows()
