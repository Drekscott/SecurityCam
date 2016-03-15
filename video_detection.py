p__author__ = 'dreytonscott'
import cv2
import numpy
import imutils
import datetime
import time
from twilio.rest import TwilioRestClient



video_capture = cv2.VideoCapture(0)
fgbgdetect = cv2.BackgroundSubtractorMOG2()
firstFrame  = None
security_text = ""
global security_time
min_area = 5000


while(True):

    ret, frame = video_capture.read()

    if not ret:
        break
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
#    gray = fgbgdetect.apply(frame)
    if firstFrame is None:
        firstFrame = gray
        continue
    frameDelta = cv2.absdiff(firstFrame,gray)
    threshold = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold,None,iterations=2)
    contours, hierarchy = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
#        if cv2.contourArea(c) < 10:
#            continue
        if cv2.contourArea(c)<500 and cv2.contourArea(c)>100:
            print "Someone is home"

        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


#    if frameDelta == 0:
#        print "No one is home"
#
#    if frameDelta == 1:
#        ret, criminalframe = video_capture.read()
#        print " criminal home"
    # loop over the contours
#    for c in cnts:
#        if frameDelta == 0:
#        # if the contour is too small, ignore it
#        if cv2.contourArea(c) < min_area:
#            continue
#
#            # compute the bounding box for the contour, draw it on the frame,
#            # and update the text
#        (x, y, w, h) = cv2.boundingRect(c)
#        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#        security_text = "Intruder in home!"
#        security_time = datetime.datetime.now()

#to check if someone is inside of the frame I need to make sure that the rectangle is less than 255. 255 is the parameter of the frame.

    if security_text is None:
         print " no one home "

    cv2.imshow("Frame Delta", frameDelta)
    cv2.imshow("Security Feed", frame)
    cv2.imshow("Threshold", threshold)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("1"):
        break

video_capture.release()
cv2.destroyAllWindows()
