## pip install opencv-python
import cv2
import os
from PIL import Image #pip install pillow
import numpy as np    # pip install numpy
from pickle import load
from datetime import datetime

Student_Data_path = "Attendance"
data = load(open("data.xml","rb"))
Lecture = input("Enter Lecture for Attendance: ")
att = []
# Add the Data Manipulation Library
import pandas as pd

time = str(datetime.now().year)+"_"+str(datetime.now().month)+"_"+str(datetime.now().day)

try:
    filname = str(os.path.join(Student_Data_path,time))+".xlsx"
    Attendance_data = pd.read_excel(filname)
except:
    Attendance_data = pd.DataFrame({"ID":[],"Name":[],"Attendance":[]})
    Attendance_data.to_excel(filname,sheet_name="Lecture "+str(Lecture),index=False)

# for i in range(len(data[0])):
#     Attendance_data.loc[i] = [data[0][i],data[1][i],"Absent"]
    
# Attendance_data.loc[len(Attendance_data)] = ["0","Suryansh","Present"]

# Attendance_data.to_excel(filname,sheet_name="Lecture 1",index=False)

# print(Attendance_data.values)

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
     
    for (x,y,w,h) in features:
        cv2.rectangle(img, (x,y), (x+w,y+h), color, 2 )
         
        id, pred = clf.predict(gray_img[y:y+h,x:x+w])
        # print(id)
        confidence = int(100*(1-pred/300))
        # print(confidence)
        if confidence>80:
                cv2.putText(img, str(Attendance_data.values.tolist()[(id-1)][1]), (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                if id not in att:
                    att.append(id)
                    print(Attendance_data.loc[id-1])
                    Attendance_data.loc[id-1] = [str(id),str(Attendance_data.values.tolist()[(id-1)][1]),"Present"]
                    Attendance_data.to_excel(filname,sheet_name="Lecture 1",index=False)
        else:
            cv2.putText(img, "UNKNOWN", (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)
     
    return img
 
# loading classifier
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
 
clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("classifier.xml")
 
video_capture = cv2.VideoCapture(0)
 
while True:
    ret, img = video_capture.read()
    img = draw_boundary(img, faceCascade, 1.3, 6, (255,255,255), "Face", clf)
    cv2.imshow("face Detection", img)
     
    if cv2.waitKey(1)==13:
        break
video_capture.release()
cv2.destroyAllWindows()