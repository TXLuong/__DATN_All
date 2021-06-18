import base64
import numpy as np
import json 
import cv2  
from io import BytesIO
import os
import datetime 
from datetime import datetime
import math
from connect_db import Connector
import time
from PIL import Image
import torch
from scipy.stats import norm
from headpose import PoseEstimator
import glob
import os
class Process_api():

    def __init__(self, name_db, face, face_anti_smoofing) :
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print("-------------------------Loadding-----------------------")
        self.anti_smoofing = face_anti_smoofing
        self.face=face
        self.threshold_distance = 1.6
        # self.connector = Connector(name_db)
        # self.detector = self.face.mtcnn
        try:
            self.labels, self.features=self.connector.get_users()
        except:
            self.features=np.array([]).reshape(0,512)
            self.features_mask=np.array([]).reshape(0,512)
            self.labels=[]
        
        print("Loaded model and database success : "+ str(self.features.shape) + ", " +str(len(self.labels)))

    def get_feature(self, image):  # input image ,output one features or no, Anh dau vao co the chua ca background 
        features, faces = self.face.feature_img(image)
        if(len(features)==1):
            return features[0]
        return None
    
    def get_feature2(self, image):  # input image ,output one features or no
        features, features_mask, faces = self.face.feature_multi(image)
        if(len(features)==1):
            return features[0], features_mask[0]
        return None, None
    
    def check_smoofing(self, face): #input face, output 1:real,0 Fake
        # return 1
        score_c, score_l, result = self.anti_smoofing.predict(face)
        if result:
            smoof_stt = "real"
            print("Real face")
            return 1
        else:
            smoof_stt = "smoofing"
            print("Fake !!!!!")
            return 0

    def img_from_base64(self, img_base64):
        img=base64.b64decode(img_base64)
        img= np.frombuffer(img, dtype=np.uint8)
        img = cv2.imdecode(img, flags=1)
        return img


    def get_all_feature(self, image) :# input image ,output all features or no
        return self.face.feature_img(image)

    def get_feature_box(self, image) : #input image , output np.array(embs), faces, bboxes
        return self.face.feature_img_test(image)

    def img_to_base64_str(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img,'RGB')
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        buffered.seek(0)
        img_byte = buffered.getvalue()
        img_str = base64.b64encode(img_byte).decode('utf-8')
        return img_str

    def img_from_base64(self, img_base64): #input base64 output img
        img=base64.b64decode(img_base64)
        img= np.frombuffer(img, dtype=np.uint8)
        img = cv2.imdecode(img, flags=1)
        return img

    def distance(self, feature1, feature2): # input f1,f2 output dis
        return np.linalg.norm(feature1 - feature2)

    
    def confidence(self, feature1, feature2):  # input f1,f2 output score
        dist = self.distance(feature1, feature2)
        if dist <= 0.7: 
            return 1.0
        elif dist <= 1.1:
            return ((1.5 - dist)/0.8)
        elif dist > 1.3: 
            return 0.0
        else:
            return ((1.3 - dist)/0.4)

    def check(self, ang):
        for x in range(3):
            if(abs(ang[x])>=85): return False
        return True
    
    
    def check_Image(self, img):
        img = cv2.resize(img,(512,512))
        detection = self.detector.detect(img)
        if(len(detection)!=1):
            return False
        else:
            angle=self.check_pose.face_orientation(detection[0][1])
            return self.check(angle)

    def identify(self, features):
        if(len(self.features)==0):
            return []
        if(len(features)==0):
            return []
        res=[]
        features= np.array(features)
        features=np.expand_dims(features, 1)
        diff = self.features - features
        dist = np.sum(np.power(diff, 2), axis=2)
        minimum = np.amin(dist, axis=1)
        min_idx = np.argmin(dist, axis=1)
        result = []
        for id,(min, min_id)  in enumerate(zip(minimum, min_idx)):          
            if min < self.threshold_distance:
                # confidence = self.confidence(features[id].reshape(512,), self.features[min_id])
                p_id = self.labels[min_id]
                res.append(p_id)
        return res
    def recognize_for_report(self, origin_features, features):
        res=[]
        features= np.array(features)
        features=np.expand_dims(features, 1)
        diff = origin_features - features
        dist = np.sum(np.power(diff, 2), axis=2)
        minimum = np.amin(dist, axis=1)
        min_idx = np.argmin(dist, axis=1)
        for id,(min, min_id)  in enumerate(zip(minimum, min_idx)):          
            if min < self.threshold_distance:
                res.append(1)
        return len(res) > 0
    def recognize_employee(self, db_features, features):
        # db_features o dang np.array
        # feature o dang list/np.array
        print("type of db_features", type(db_features))
        res=[]
        features= np.array(features)
        features=np.expand_dims(features, 1)
        diff = db_features - features
        dist = np.sum(np.power(diff, 2), axis=2)
        minimum = np.amin(dist, axis=1)
        min_idx = np.argmin(dist, axis=1)
        print("diff : ", diff)
        for id,(min, min_id)  in enumerate(zip(minimum, min_idx)):          
            if min < self.threshold_distance:
                res.append("Identity_of_employee")
                print("min : ", min)
        print("res recognization : ", res)
        return res
    def identify_mask(self, features):
        if(len(self.features_mask)==0):
            return []
        if(len(features)==0):
            return []
        res=[]
        features= np.array(features)
        features=np.expand_dims(features, 1)
        diff = self.features_mask - features
        dist = np.sum(np.power(diff, 2), axis=2)
        minimum = np.amin(dist, axis=1)
        min_idx = np.argmin(dist, axis=1)
        result = []
        for id,(min, min_id)  in enumerate(zip(minimum, min_idx)):          
            if min < self.threshold_distance:
                # confidence = self.confidence(features[id].reshape(512,), self.features[min_id])
                p_id = self.labels[min_id]
                res.append(p_id)
        return res

    def add_attendance(self,faces):
        id_emps=self.identify(self.face.features_from_faces(faces))
        res=""
        for id_emp in id_emps:
            res+=id_emp+","
        if(res!=""):
            return res[:-1]
        return ""
    def add_worklog(self,db_face,faces):
        print("type face of last moment", type(faces))
        id_emps=self.recognize_employee(db_face, self.face.features_from_faces([faces]))
        return len(id_emps) > 0
    def add_attendance_pi(self,img):
        # get face and 
        features, faces=self.face.feature_img(img)
        feas = []
        for (face, feature) in zip(faces, features) :
            if self.check_smoofing(face):
                feas.append(feature)
        id_emps=self.identify(feas)
        res=""
        id=0
        for id_emp in id_emps:
            # if(self.check_smoofing(face)):
            #     res.append(id_emp+"_"+"real")
            # else:
            #     res.append(id_emp+"_"+"fake")
            res+=id_emp+","

        if(res!=""):
            return res[:-1]
        return ""


    def add_employee(self,id_emp,img):
        # id of employee and img 
        if(img is not None):
            # get feature from employee image
            feature = self.get_feature(img)
            if(feature is not None):
                self.features = np.concatenate((self.features, feature.reshape(1, 512)))
                self.labels.append(id_emp)
                print("Add new success : "+ str(id_emp) + ", "+ str(self.features.shape) + ", " +str(len(self.labels)))
                self.connector.add_user(id_emp,feature.tolist())
                return feature
            return None
        return None
    # def extract_features(self, img):
    #     feature = self.get_feature(img)
    # anh dau vao co the la anh chua ca background va face 
    def extract_features(self, im_b64):
        parts = im_b64.split(",")
        print("len ----- ", len(parts))
        base64String = parts[1]
        print("base64 string")
        print(base64String)
        image = self.img_from_base64(base64String)
        feature = self.get_feature(image)
        print(type(feature))
        print(feature.shape)
        print(feature)
        return feature
    





        


    
