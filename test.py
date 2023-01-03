##########################################
#                                        #
# NOTE: using Windows cmd instead of wsl #
#                                        #
##########################################
import cv2
import numpy as np

video = cv2.VideoCapture("Shot 1 - Mama.mp4")
# video2 = cv2.VideoCapture("")
 
while True:
 
    ret, frame = video.read()
 
    frame = cv2.resize(frame, (1280, 720))
 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    lower_green = np.array([25, 52, 72])
    upper_green = np.array([102, 255, 255])
 
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    mask = cv2.bitwise_not(mask)

    res = cv2.bitwise_and(frame, frame, mask = mask)
 
    f = frame - res
 
    cv2.imshow("video", frame)
    cv2.imshow("mask", f)
    cv2.imshow("result", res)
 
    # escape key?
    if cv2.waitKey(25) == 27:
        break
 
video.release()
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)