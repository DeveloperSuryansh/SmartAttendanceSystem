## pip install opencv-python
from pickle import dump,load
import cv2
import os
from PIL import Image #pip install pillow
import numpy as np    # pip install numpy
import pandas as pd

from datetime import datetime

Student_Data_path = "Attendance"

def train_classifier(data_dir):
    path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
    faces = []
    ids = []
    
    time = str(datetime.now().year)+"_"+str(datetime.now().month)+"_"+str(datetime.now().day)

    try:
        filname = str(os.path.join(Student_Data_path,time))+".xlsx"
        Attendance_data = pd.read_excel(filname)
    except:
        print("First run the Generate.py File")
        exit(1)

    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])
        faces.append(imageNp)
        ids.append(id)

    ids = np.array(ids)
    # Train and save classifier
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces,ids)
    # dump(file = open("classifier.xml","wb"),obj = clf)
    clf.write("classifier.xml")

train_classifier("data")
