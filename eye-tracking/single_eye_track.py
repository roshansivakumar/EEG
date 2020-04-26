#import libraries
import numpy as np
import cv2
import xlwt
from xlwt import Workbook
import datetime

#detect faces
def detect_faces(img, cascade):
    if img is not None:
        #change to gray scale for easier analysis
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #detect faces with cascade
        faces = cascade.detectMultiScale(gray_frame, 1.3, 5)
        #draws rectangle around face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 0), 2)
            face = img[y:y + h, x:x + w]
        return face

#detect eyes
def detect_eyes(face, cascade):
    #gray scales the image
    gray_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    #detects eys with cascade
    eyes = cascade.detectMultiScale(gray_face, 1.3, 5)
    #finds heights and width of face frame
    width = np.size(face, 1)
    height = np.size(face, 0)
    left_eye = None
    right_eye = None
    for (x, y, w, h) in eyes:
        if y < height / 2:
            #displays rectangle around eyes
            #cv2.rectangle(face, (x, y), (x+w, y+h), (0, 255, 255), 2)
        # For detecting left and right eye to help spot pupil
            eyecenter = x + w / 2
            if eyecenter < width * 0.5:
                left_eye = face[y:y + h, x:x + w]
                #displays rectangle around left eye
                cv2.rectangle(face, (x, y), (x+w, y+h), (0, 255, 255), 2)
            else:
                right_eye = face[y:y + h, x:x + w]
    return left_eye, right_eye

#clean up image by cutting out the eyebrow
def cut_eyebrows(img):
    #cuts eyebrows from the top of the eye rectangle
    height, width = img.shape[:2]
    eyebrow_h = int(height/4)
    img = img[eyebrow_h:height, 0:width]
    return img

#returns keypoints on the pupil
def blob_process(img, detector):
    #gray scales image then changes binary threshold to make pupil stick out
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_frame, 52, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2) #1
    img = cv2.dilate(img, None, iterations=4) #2
    img = cv2.medianBlur(img, 5) #3
    #detects keypoints of the pupil
    keypoints = detector.detect(img)

    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    copy = img
    c = cv2.drawContours(copy, contours, 0, (255,255,0), 2)
    center = (copy, contours)
    #cv2.imshow('copy', copy)
    #print ("Contours,", contours[1])
    if len(contours) == 2:
        return contours[1]
    if len(contours) == 1:
        return contours[0]

#draw cross on pupil
def cross(img, contour):
    #find center of the contour
    M = cv2.moments(contour)
    cX = int(M["m10"]/M["m00"])
    cY = int(M["m01"]/M["m00"])

    #draw the contour and center of the shape
    cv2.circle(img, (cX, cY), 4, (255,0,0), 2)
    cv2.drawContours(img, contour, -1, (255,0,0), 2)
    cv2.line(img, (cX-10, cY), (cX+10, cY) , (0,0,255), 2)
    cv2.line(img, (cX, cY-10), (cX, cY+10), (0,0,255), 2)
    #display image
    return cX,cY

#read video file
cap = cv2.VideoCapture('video.avi')
#create workbook
workbook = Workbook()
worksheet = workbook.add_sheet('Sheet 1')

#start from first column and row
row = 0
col = 0

#initilizing blobs
detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector_params.minArea = 40
detector = cv2.SimpleBlobDetector_create(detector_params)

#classifiers
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

worksheet.write(row, col, "cX")
worksheet.write(row, col+1, "cY")
row += 1

#framecount
count = 1
#center points
cXmax = 0 #min it could be
cXmin = 255 #max it could be
cYmax = 0
cYmin = 255

#movement counts
xDeviation = 0
yDeviation = 0
bothDeviation = 0

#run while video is open
while(cap.isOpened()):
    #analysis of each frame
    ret, frames = cap.read()
    faces = detect_faces(frames, face_cascade)
    if faces is not None:
        eyes = detect_eyes(faces, eye_cascade)
        left = eyes[0]
        if left is not None:
            left = cut_eyebrows(left)
            keypoints = blob_process(left, detector)
            #left = cv2.drawKeypoints(left, keypoints, left, (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            if keypoints is not None:
                left = cv2.drawContours(left, keypoints, -1, (255,255,0), 2)

                cv2.imshow('frame', frames)
                #print(left)
                center = cross(left, keypoints)
                print("Center, ", center)
                worksheet.write(row, col  , center[0])
                worksheet.write(row, col+1, center[1])

                #sets range for non movement
                if count <= 20:
                    if center[0] > cXmax:
                        cXmax = center[0]
                    if center[0] < cXmin:
                        cXmin = center[0]
                    if center[1] > cYmax:
                        cYmax = center[1]
                    if center[1] < cYmin:
                        cYmin = center[1]
                else:
                    print("DID THEY MOVE?")
                    if center[0] > cXmax:
                        if center[1] > cYmax:
                            print("DEVIATION")
                            bothDeviation += 1
                            worksheet.write(row, col+2, "DEVIATION")
                        elif center[1] < cYmin:
                            print("DEVIATION")
                            bothDeviation += 1
                            worksheet.write(row, col+2, "DEVIATION")
                        else:
                            print("XDEVIATION")
                            xDeviation += 1
                            worksheet.write(row, col+2, "XDEVIATION")
                    elif center[0] < cXmin:
                        if center[1] > cYmax:
                            print("DEVIATION")
                            bothDeviation += 1
                            worksheet.write(row, col+2, "DEVIATION")
                        elif center[1] < cYmin:
                            print("DEVIATION")
                            bothDeviation += 1
                            worksheet.write(row, col+2, "DEVIATION")
                        else:
                            print("XDEVIATION")
                            xDeviation += 1
                            worksheet.write(row, col+2, "XDEVIATION")
                    else:
                        if center[1] > cYmax:
                            print("XDEVIATION")
                            yDeviation += 1
                            worksheet.write(row, col+2, "YDEVIATION")
                        elif center[1] < cYmin:
                            print("YDEVIATION")
                            yDeviation += 1
                            worksheet.write(row, col+2, "YDEVIATION")


    datet = str(datetime.datetime.now())
    worksheet.write(row, col+3, datet)
    row += 1

    count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(count)
print(cXmax, cXmin)
print(cYmax, cYmin)
print(xDeviation, yDeviation, bothDeviation)


workbook.save('LeftEye2.xls')
cap.releaser()
cv2.destroyAllWindows()
