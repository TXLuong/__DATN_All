import cv2
import json
import torch
from anti_track import Anti_smoofing_track
from functools import wraps
from bson import json_util, ObjectId
from face.face_process import face_recognize
from support_api import Process_api
import pickle
import time
import math
from io import BytesIO
from PIL import Image
import numpy as np
import base64
from flask import Flask, render_template, request, jsonify
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# --------------------------------------------"FACE_APPLICATION"--------------------------------------
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
face = face_recognize()
face_anti_smoofing = Anti_smoofing_track(device)

app = Flask(__name__)

process_api = Process_api("recognize_mask", face, face_anti_smoofing)


# kiem ta that hay khong 
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    r = request.json
    faces = []
    faces_mask = []
    t1 = time.time()
    id_emps=""
    for x in r['image']:
        img = process_api.img_from_base64(x)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        if process_api.check_smoofing(im_pil) :
                faces.append(im_pil)
    if(len(faces) > 0) or (len(faces_mask) > 0):
        id_emps=process_api.add_attendance(faces)
    print(time.time() - t1)
    return id_emps


@app.route('/attendance_pi', methods=['GET', 'POST'])
def attendance_pi():
    r = request.json
    t1 = time.time()
    id_emps=""
    img = process_api.img_from_base64(r['image'])
    id_emps=process_api.add_attendance_pi(img)
    return id_emps

@app.route('/employee', methods=['GET', 'POST'])
def employee():
        r = request.json
        id_emp = r['name']
        base64=r['base64']
        image = process_api.img_from_base64(base64)
        feature = process_api.add_employee(id_emp, image)
        if(feature is  None):
            return json.dumps({"stt" : "1", "msg" : "Add error, no face or more than one face"})
        return json.dumps({"stt" : "0", "msg" : "Add sucess"})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", threaded=False, port=3007)
