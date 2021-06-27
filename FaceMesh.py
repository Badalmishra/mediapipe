import cv2
import mediapipe as mp
import pyautogui
import scipy.interpolate
import math
width,height =pyautogui.size()
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
print('height,width',height,width)
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
# pyautogui.moveTo(width-(width/4),height/2)
originRect = False
origin=False
offset = 50
endPoint =(offset,offset)
startPoint =(0,0)
def getScaledCoordinates(point,image):
    x, y = point.x, point.y
    shape = image.shape
    x = int(x * shape[1])-10
    y = int(y * shape[0])
    return [x,y]

def getScreenScaledPoints(pointX,pointY,image):
    xCamRange =(int(startPoint[0]),endPoint)
    xScreenRange = (0,int(width/2))
    xInterpolate = scipy.interpolate.interp1d((0,5),(7,12))
    errorX =origin[0]
    errorY =origin[1]
    x =int((pointX)*(width/2))
    y =int((pointY)*height)


    # x = int((x * width)/2 )
    # y = int( y * (height) )
    return [x,y]
lastX = 0
lastY = 0
counter = 0
with mp_face_mesh.FaceMesh(
    min_detection_confidence=1,
    min_tracking_confidence=0.2) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
          point = face_landmarks.landmark[1]
          printX,printY=getScaledCoordinates(point,image)
          if (originRect == False):
              print('origin',point)
              originRect = [printX, printY]
              origin = [point.x, point.y]
              startPoint = (originRect[0] - offset, originRect[1] - offset)
              endPoint = (originRect[0] + offset, originRect[1] + offset)
          cv2.putText(image,".", (int(printX), int(printY)), cv2.FONT_HERSHEY_COMPLEX,
                      2, (255, 0, 0), 3)

          if (origin != False):
              color = (225, 225, 0)
              if(printX>endPoint[0] or printX<startPoint[0] or printY<startPoint[1] or printY>endPoint[1] ):
                color = (0,0,225)
              else:
                  cv2.line(image, (startPoint[0], printY), (printX, printY), (10, 10, 123), 3)
                  cv2.line(image, (printX, startPoint[1]), (printX, printY), (10, 10, 123), 3)
                  lenX = ((printX-startPoint[0])/offset*50)
                  lenY = ((printY-startPoint[1])/offset*50)

                  print('lenX',lenX,lastX)
                  print('lenY',lenY,lastY)

                  cv2.putText(image, str(lenX), (int(startPoint[0]), int(printY)), cv2.FONT_HERSHEY_COMPLEX,
                              0.4, (25, 220, 0), 1)
                  cv2.putText(image, str(counter), (int(printX), int(startPoint[1])), cv2.FONT_HERSHEY_COMPLEX,
                              0.4, (25, 220, 0), 1)
                  if(lenX>=lastX+1 or lenX<=lastX-1 or lenY>=lastY+1 or lenY<=lastY-1 or lastX == 0 or lastY==0) :
                      screenX = (width/2)/100*lenX
                      screenY = (height)/100*lenY
                      pyautogui.moveTo(screenX-10, screenY-10)
                  if (lenX >= lastX + 4 or lenX <= lastX - 4 or lenY >= lastY + 4 or lenY <= lastY - 4 or lastX == 0 or lastY == 0):
                      counter = 0
                  else:
                      counter+=1
                      if(counter>=50):
                          pyautogui.doubleClick()
                  lastX = lenX
                  lastY = lenY
              cv2.rectangle(image, startPoint, endPoint, color, 2)

    cv2.imshow('MediaPipe FaceMesh', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
