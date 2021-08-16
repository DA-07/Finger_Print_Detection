import cv2
import numpy as np
import utilities
import time
import random as rng
camera=1
frameWidth = 426
frameHeight = 240

cap= cv2.VideoCapture(camera)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
utilities.initializeTrackBar()

pTime=0
cTime=0
font = cv2.FONT_HERSHEY_PLAIN

while True:
    _,img = cap.read()
    result = img.copy()
    h, w,c = img.shape
    print(img.shape)

    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    val = utilities.getTrackbarValues()
    mask = cv2.inRange(hsv_img, val[0], val[1])

    # medianBlur(Handed_Thres, Handed_Thres, 7);
    median = cv2.medianBlur(mask, 5)
    kernel = np.ones((5, 5), np.uint8)

    '''opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
       This can also be used'''

    img_erosion = cv2.erode(median, kernel, iterations=2)
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=2)
    mask=img_dilation

    # mask = cv2.rectangle(mask,(0,0),(80,h),(0,0,0),-1)
    # mask = cv2.rectangle(mask, (0,h-150), (w,h), (0, 0, 0), -1)
    # mask = cv2.rectangle(mask, (w-80, 0), (w,h), (0, 0, 0), -1)
    # mask = cv2.rectangle(mask, (0, 0), (w, 50), (0, 0, 0), -1)
    # cv2.line(img, (80, 50), (80, h-150), (0, 0, 255), 1)
    # cv2.line(img, (80, h-150), (w-80, h-150), (0, 0, 255), 1)
    # cv2.line(img, (w-80, h-150), (w - 80, 50), (0, 0, 255), 1)
    # cv2.line(img, (0,50 ), (w, 50), (0, 0, 255), 5)
    #coloredMask= mask * img
    edges = cv2.Canny(mask, 100, 200)# threshold = 100 ,and *2



    #Contour detection :

    # For openCV version 2 or 4
    if cv2.getVersionMajor() in [2, 4]:
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        numOfCnt= len(contours)

    else:
    # For OpenCV 3
        _, contours, _ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        numOfCnt = len(contours)

    # height=h
    # while (numOfCnt >= 0) and (numOfCnt < 5) and h>0 :
    #
    #     mask = cv2.line(mask, (height, 0),(w,h) ,(0,0,0), 1)
    #     height=height-1



    #finding rotated rectangles

    for c in contours:
        area = cv2.contourArea(c)
        #normal Rectangle:
        #if cv2.contourArea(c)
        height = h
        if area <500:
            break
        elif (area < 15000) and (area >= 500 ):
             #print(area)
             #continue
             # (x,y,w,h)= cv2.boundingRect(c)
             # cv2.rectangle(img, (x,y), (x+w,y+h),(0,255,0),2)

             while (numOfCnt >= 0) and (numOfCnt < 5) and h>0:
                 mask = cv2.line(mask, (0, height),(w,height) ,(0,0,0), 20)
                 height=height-20
             #rotated rectangle:
             rect = cv2.minAreaRect(c)
             #print(rect)
             box = cv2.boxPoints(rect)
             box = np.int0(box)
             cv2.drawContours(img,[box],0,(0,191,255),2)

    #blankImg = np.zeros((426, 240, 3), np.uint8)
    cv2.putText(mask,"To Quit press 'q'",(40,70),2,2,(255,255,255),2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "FPS: " + str(fps), (12, 30), font, 1.0, (32, 32, 32), 4, cv2.LINE_AA)
    cv2.putText(img, "FPS: " + str(fps), (11, 30), font, 1.0, (240, 240, 240), 1, cv2.LINE_AA)

    stack = utilities.imgStack(1.0, ([img, mask], [hsv_img, edges]))
    cv2.imshow('Outputs', stack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()