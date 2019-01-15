import numpy as np
import os
import cv2
import pickle
import mongoConnect

filename = 'video.avi'
frames_per_second = 24.0
res = '720p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")
labels = {}
NameID = [] #this will be used to determine if we've seen a label.
NameIDCounter = {}  #Dictionary that is used to count the number of times we record a label
confidenceBool = True #sets to false once our NameIDCounter exceeds or matches CONST_CONFIDENCE_NUM
CONST_CONFIDENCE_NUM = 10 # if our label reaches 10 or more then we can be reach to DB
personToPass = ''   #string value that we need to pass to our db connection script.
with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)
#out = cv2.VideoWriter(filename, get_video_type(filename), frames_per_second, get_dims(cap, res))

while confidenceBool:
    ret, frame = cap.read()
    #out.write(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    #out.write(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    #iterate through faces
    for(x, y, w, h) in faces:
        #print(x,y,w,h)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        id_, conf = recognizer.predict(roi_gray) #return label and confidence
        if conf >=40:
            #print(id_)
            #instead of printing the id, lets append it to an array.
            print(labels[id_])
            #NameID = {labels[id_]: 0}
            if not labels[id_] in NameID:
                NameID.append(labels[id_])
                NameIDCounter[labels[id_]] = 0

            NameIDCounter[labels[id_]] += 1
            print(NameIDCounter[labels[id_]])

            if NameIDCounter[labels[id_]] >= CONST_CONFIDENCE_NUM:
                confidenceBool = False
                personToPass = labels[id_]

            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

        #print(conf)
        #img_item = "my-image.png"
        #cv2.imwrite(img_item, roi_gray)

        color = (0, 0, 255)
        stroke = 3
        end_cord_x = x+w
        end_cord_y = y+h
        cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke) #boxes face
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for(ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 255), 2) #boxes eyes
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if len(personToPass) > 0:
    print(personToPass)
    val = mongoConnect.main(personToPass) #executes our mongoconnect script with our desired argument.
cap.release()
#out.release()
cv2.destroyAllWindows()
