import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math

################################
wCam, hCam = 1200, 600
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

print(detector)
vol = 0
volBar = 400
volPer = 0
drawPoints = []
mode=''
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList,bbox = detector.findPosition(img, draw=False)
    for point in drawPoints:
        cv2.circle(img, (point[0], point[1]), 3, (0, 0, 255), cv2.FILLED)

    if len(lmList) > 20:


        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[12][1], lmList[12][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        cv2.circle(img, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        eraserX1, eraserY1 = lmList[16][1], lmList[16][2]
        eraserX2, eraserY2 = lmList[12][1], lmList[12][2]
        eraserCx, eraserCy = (eraserX1 + eraserX2) // 2, (eraserY1 + eraserY2) // 2
        cv2.line(img, (eraserX1, eraserY1), (eraserX2, eraserY2), (123, 0, 123), 3)

        eraserLength = math.hypot(eraserX2 - eraserX1, eraserY2 - eraserY1)




        if length < 50 and eraserLength>50:
            mode = "pencil"
            print('drawPoints', len(drawPoints))
            drawPoints.append([cx,cy])
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        if eraserLength < 50:
            mode = "eraser"
            cv2.line(img, (eraserX1, eraserY1), (eraserX2, eraserY2), (10, 10, 123), 3)
            for point in drawPoints:
                print(point[0],[eraserX1,eraserX2])
                if point[0] > (eraserX1-15) and point[0] < (eraserX2+15) and point[1] < (eraserY1+15) and point[1] > (eraserY2-15) :
                    print('===')
                    drawPoints.remove(point)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    img = cv2.flip(img, 1)
    cv2.putText(img, f'Mode: {mode}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)