## pip install opencv-python
import cv2
import os
from PIL import Image #pip install pillow
import numpy as np    # pip install numpy
from pickle import dump,load
from datetime import datetime

Student_Data_path = "Attendance"

# Add the Data Manipulation Library
import pandas as pd

time = str(datetime.now().year)+"_"+str(datetime.now().month)+"_"+str(datetime.now().day)

try:
    filname = str(os.path.join(Student_Data_path,time))+".xlsx"
    Attendance_data = pd.read_excel(filname)
except:
    Attendance_data = pd.DataFrame({"ID":[],"Name":[],"Attendance":[]})
    Attendance_data.to_excel(filname,sheet_name="Lecture 1",index=False)

################################


data_dir = "data"

def print_dataset():
    for d in range(len(Attendance_data)):
        print(Attendance_data.values.tolist()[d][0],Attendance_data.values.tolist()[d][1],sep=" => ")

def delete_dataset(id):
    # try:
        Attendance_data.loc[int(id)-1] = ["","",""]
        for i in os.listdir(data_dir):
            id_delete = i.split(".")
            if id_delete[1] == str(id):
                os.remove(os.path.join(data_dir,i))
        Attendance_data.to_excel(filname,sheet_name="Lecture 1",index=False)
        os.system("python Trainer.py")
    # except:
        # print("User not Exist")

def generate_dataset():
    face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    def face_cropped(img):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        # scaling factor = 1.3
        # minimum neighbor = 5
         
        if faces is ():
            return None
        for (x,y,w,h) in faces:
            cropped_face = img[y:y+h,x:x+w]
        return cropped_face
     
    cap = cv2.VideoCapture(0)
    name = input("Enter here Name: ")
    id = input("Enter here ID:")
    Attendance_data.loc[len(Attendance_data)] = [str(id),str(name),"Absent"]
    Attendance_data.to_excel(str(os.path.join(Student_Data_path,time))+".xlsx",index=False)
    img_id = 0
    
    while True:
        ret, frame = cap.read()
        if face_cropped(frame) is not None:
            img_id+=1
            face = cv2.resize(face_cropped(frame), (200,200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_name_path = "data/user."+str(id)+"."+str(img_id)+".jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(img_id), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            
            cv2.imshow("Cropped face", face)
             
        if cv2.waitKey(1)==13 or int(img_id)==200: #13 is the ASCII character of Enter
            break
             
    cap.release()
    cv2.destroyAllWindows()
    print("Collecting samples is completed....")

print(""" 
        Enter 1) To Add Student Data
        Enter 2) To Delete Students Data and Update Classifier
        Enter 3) To Print the Data
    """)

num = input()
if int(num) == 1:
    generate_dataset()
if int(num) == 2:
    delete_dataset(input("Enter ID of the student: "))
if int(num) == 3:
    print_dataset()