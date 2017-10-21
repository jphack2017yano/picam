# -*- coding: utf-8 -*-
import cv2
import sys

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
        # cv2.rectangle(human_area[rel_max_ind], (0, 0), human_area[rel_max_ind].shape[:2],(255,50,0), 3)
        # cv2.rectangle(im, (human_area[rel_max_ind]['x'], human_area[rel_max_ind]['y']), human_area[rel_max_ind]['img'].shape[:2], (255, 50, 0), 3)
        cv2.circle( im, ( human_area[rel_max_ind]['x'] + int(human_area[rel_max_ind]['img'].shape[1]/2), human_area[rel_max_ind]['y'] + int(human_area[rel_max_ind]['img'].shape[0]/2)), 5, (255, 50, 0), 3)

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
