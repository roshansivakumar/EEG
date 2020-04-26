#library importing
import scipy
from scipy.spatial import distance as dist
import numpy as np
import imutils
from imutils import face_utils
import time
import cv2
from imutils import face_utils
import argparse

def eye_aspect_ratio(eye):
    #compute euclidean distances between vertical landmarks
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    #compute euclidean distance between horizontal landmarks
    C = dist.euclidean(eye[0], eye[3])

    #find aspect ratio
    ear = (A + B) / (2.0 * C)

    return ear

"""
#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required = True, help = "path to facial landmark predictor")
ap.add_argument("-v", "--video", type = str, default = "", help = "path to input video file")
args = vars(ap.parse_args())
"""

#defines 2 constants for eye ratio to indicate blinks
#and then a second for number of consectuive frames that eye must be below threshold
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3

#initialize frame counters and number of blinks
frame_counter = 0
blinks = 0

#initialize dlib's face detector and create landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

#grab indexes of the facial landmarks fro left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

#starts video stream
cap = cv2.VideoCapture(0)

#creates writer for video stream
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('faceRecording2.avi', fourcc, 20.0, (640,480))

#loops frame for video stream
while True:
    #takes frame capture
    ret, frame = cap.read()
    frame = imutils.resize(frame, width = 450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #detects faces in grayscale frame
    rects = detector(gray, 0)

    #loops over the face detections
    for rect in rects:
        #determine facial landmarks then convert to x,y coordinates
        shape = predictor (gray, rect)
        shape = face_utils.shape_to_np(shape)

        #coordinates left and right eye and compute aspect ratios
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        #compute the convex hull for eyes, and visulize each
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0,255,0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0,255,0), 1)

        #check if EAR is below blink threshold
        if ear < EYE_AR_THRESH:
            frame_counter += 1

        else:
            if frame_counter >= EYE_AR_CONSEC_FRAMES:
                blinks += 1

        frame_counter = 0

        cv2.putText(frame, "Blinks : {}".format(blinks), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        cv2.putText(frame, "EAR : {.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    cv2.imshow("Frame", frame)

    #exits screen
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

#release stream and destroys windows
cap.release()
cv2.destroyAllWindows()
