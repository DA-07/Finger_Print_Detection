import cv2
import numpy as np

def callback(x):
    pass


def initializeTrackBar():
    """This"""
    cv2.namedWindow("HSV_TRACKBAR")
    cv2.resizeWindow("HSV_TRACKBAR", 640, 240)
    ilowH = 0
    ihighH = 179
    ilowS = 60
    ihighS = 255
    ilowV = 30
    ihighV = 255

    cv2.createTrackbar('lowH', 'HSV_TRACKBAR', ilowH, 179, callback)
    cv2.createTrackbar('highH', 'HSV_TRACKBAR', ihighH, 179, callback)

    cv2.createTrackbar('lowS', 'HSV_TRACKBAR', ilowS, 255, callback)
    cv2.createTrackbar('highS', 'HSV_TRACKBAR', ihighS, 255, callback)

    cv2.createTrackbar('lowV', 'HSV_TRACKBAR', ilowV, 255, callback)
    cv2.createTrackbar('highV', 'HSV_TRACKBAR', ihighV, 255, callback)

def getTrackbarValues():
    """This"""
    hL = cv2.getTrackbarPos('lowH', 'HSV_TRACKBAR')
    hH = cv2.getTrackbarPos('highH', 'HSV_TRACKBAR')
    sL = cv2.getTrackbarPos('lowS', 'HSV_TRACKBAR')
    sH = cv2.getTrackbarPos('highS', 'HSV_TRACKBAR')
    vL = cv2.getTrackbarPos('lowV', 'HSV_TRACKBAR')
    vH = cv2.getTrackbarPos('highV', 'HSV_TRACKBAR')
    lower_hsv = np.array([hL, sL, vL], np.uint8)
    higher_hsv = np.array([hH, sH, vH], np.uint8)
    vals = [lower_hsv,higher_hsv]
    return vals

#image stacking for better visualization

def imgStack(scale,imgArray):
    """This"""
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

