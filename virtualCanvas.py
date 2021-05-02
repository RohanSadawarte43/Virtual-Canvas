import cv2
import numpy as np

#yellow 24 37 81 255 0 255
#blue 108 118 156 255 0 255
#green 62 94 105 255 0 255

mycolors = [["Yellow",24, 37, 81, 255, 0, 255],
          ["Blue",108, 118, 156, 255, 0, 255],
          ["Green",62, 94, 105, 255, 0, 255]]

myColorValues = [[0,255,255],
             [112,25,25,],
             [0,100,0]]

myPoints = [] #(x, y, color)

def findColor(img,mycolors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints=[]
    for clr in mycolors:
        lower = np.array(clr[1:7:2])
        higher = np.array(clr[2:7:2])
          mask = cv2.inRange(imgHSV, lower, higher)
        # cv2.imshow(str(clr[0]),mask)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
    return newPoints

def getContours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w =0,0,0
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        if peri > 150:
            area = cv2.contourArea(cnt)
            cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect((approx))
    return (x+w//2,y)

def drawOnCanvas(myPoints, myColorValues):
    for points in myPoints:
        cv2.circle(imgResult, (points[0],points[1]), 10, myColorValues[points[2]], cv2.FILLED)


cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,10)

while True :
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img,mycolors,myColorValues)
    if (len(newPoints) != 0):
        for pts in newPoints:
            myPoints.append(pts)
    if (len(newPoints) != 0):
        drawOnCanvas(myPoints,myColorValues)
    cv2.imshow("Video",imgResult)
    if cv2.waitKey(10) & 0xFF ==ord('q'):
        break
