import os.path
from re import A
import cv2
from cv2 import data
from numpy.lib.utils import info
from numpy.testing._private.utils import print_assert_equal
from service import MonitorService
import os
from flask import Flask, request, render_template, send_from_directory, jsonify, make_response, Response
import jwt
import datetime
from flask_cors import CORS, cross_origin
import base64
from service import MonitorService 
import json
from face.face_process import face_recognize
from anti_track import Anti_smoofing_track
import torch
import sys 
import os
from utils import Utils
from support_api import Process_api
from PIL import Image
import numpy as np 
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# ----------------------------------------------------------------
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
face = face_recognize()
util_functions = Utils()
face_anti_smoofing = Anti_smoofing_track(device)
process_api = Process_api("recognize_mask", face, face_anti_smoofing)

app = Flask(__name__)
api_login = {
    "origins": ["http://localhost:3000"],
    "methods" : ["Options", "GET", "POST"],
    "allow_headers" : ["authorization"]
}
# CORS(app, resources={
#     r'/login' : api_login
# }
# )
# CORS(app, resources=r'/current')
# CORS(app, resources=r'/logout')
# CORS(app, resources=r'/turnIn')
# CORS(app, resources=r'/addEmployee')
# CORS(app, resources=r'/profile')
# CORS(app, resources=r'/password')
# CORS(app, resources=r'/employee/history')

app.config['SECRET_KEY'] ='thisisthesecretkey'
# APP_ROOT = os.path.dirname(os.path.abspath(__file__))

service = MonitorService(face, face_anti_smoofing)

# service.checkLogin("acds","acscscd")

@app.route("/monitor/create", methods=["POST"])
def create_monitor():
    data = request.get_json()
    print("----------------",type(data))
    monitor = data 
    service.create_monitor(monitor)
    return data

@app.route("/monitors", methods=["GET"])
def getlist():
    data = service.get_monitors()
    print(type(data))
    return jsonify(data)

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
    execution_path = target
    print(execution_path)
    image = Predict(os.path.join(execution_path, filename))
    print(image.shape)
    print('predicted')
    out_image = cv2.imwrite(os.path.join(execution_path,  "flask"+filename), image)
    print('wrote out the image')
    print('flask'+filename)
    return render_template("Flask_FacialRecognition_WebService.html", image_name="flask"+filename)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/login', methods = ['POST'])
# @cross_origin()
def login():
    # de username va password trong header
    headers = request.headers.get("Authorization")
    transform = base64.b64decode(headers)
    res = transform.decode("UTF-8")
    arr = res.split(":")
    auth = {"email" : arr[0], "password" : arr[1]}
    check, roleid = service.checkLogin(auth['email'], auth['password'])
    print("display roleid : ", roleid)
    print("auth : ", auth)
    print("check : ", check)
    if auth and check :
        # verify who user is 
        token = jwt.encode({'user': auth['email'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60*12)}, app.config['SECRET_KEY'])
        res  = jsonify({"token": token.decode('UTF-8'),"roleid" : roleid})
        return make_response(res, 200, {'Access-Control-Allow-Origin' : '*','Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,OPTIONS','Access-Control-Allow-Headers' : 'Content-Type,Authorization','Access-Control-Allow-Origin': '*'})
 
    return make_response('Could not verify', 401, {'Access-Control-Allow-Origin' : '*','Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,OPTIONS','Access-Control-Allow-Headers' : 'Content-Type,Authorization'})


@app.route("/workLog/create", methods=["POST"])
def workLog():
    data = request.json
    # data = jsonify(data)
    print("recieved data ", data['time'])
    print(type(data))
    service.addWorkLog(data)
    return data

@app.route("/current", methods=["POST"])
def getCurrent():
    # lay token 
    user_type = request.json
    token = request.headers.get("X-Auth-Token")
    auth = jwt.decode(token, app.config['SECRET_KEY'])
    if user_type == "Monitor":
        data = service.find_monitor_by_email(auth['user'])
        print(data)
        print("auth", auth)
        print(service.find_monitor_by_email(auth['user']))
        return util_functions.convert_to_monitor(data)
    else : 
        data = service.find_employee_by_email(auth['user'])
        return util_functions.convert_to_monitor(data)
    # return {"username" : "luong","password" : "luong", "firstname" : "luong","email" : "lu@gmail.com"}

@app.route("/logout", methods=["POST"])
def logout():
    # set refresh token to null
    return "ok"

@app.route("/turnIn", methods=["POST"])
def turnIn():
    token = request.headers.get("X-Auth-Token") 
    auth = jwt.decode(token,app.config['SECRET_KEY'])
    imageBase64 = request.json
    parts = imageBase64.split(",")
    base64String = parts[1]
    print(auth)
    print(type(auth))
    img = process_api.img_from_base64(base64String)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    success = process_api.check_smoofing(im_pil)
    print("success status ", success)
    data = service.get_feature_from_db(auth['user'])
    res = process_api.add_worklog(np.array(data[0][0]),im_pil)
    if res:
        service.check_and_add_work_log(auth=auth, imageBase64=imageBase64, success=success)
    else:
        print("Khong phai user dang su dung")
        return "err"
    return "ok"

@app.route("/addEmployee", methods=["POST"])
def addFace():
    res = request.json
    img_base64 = res['face']
    infor = res['infor']
    feature = process_api.extract_features(img_base64)
    service.save_new_employees(feature, infor)
    return {"status" : "ok"}

@app.route("/profile", methods=["POST"])
def change_profile():
    data = request.json
    if data['role'] == "Monitor":
        service.change_monitor_profile(data)
        return "modified monitor"
    elif data['role'] == "Employee":
        service.change_employee_profile(data)
        return "modified employee"
    return "error occured"
@app.route("/password", methods=["POST"])
def change_password():
    data = request.json
    if data['role'] == "Employee":
        employee = service.find_employee_by_id(data['id'])
        if employee != None and employee[1] == data['oldPassword']:
            print("find employee with oldPassword")
            service.change_employee_password(data)
            return {"message":"changed employee password"}
    elif data['role'] == "Monitor":
        monitor = service.find_monitor_by_id(data['id'])
        if monitor != None and monitor[1] == data['oldPassword']:
            print("find monitor with oldPassword")
            service.change_monitor_password(data)
            return {"message" : "changed monitor's password"}
    return {"message" : "error occured"}
@app.route("/employee/history", methods = ["POST"])
def employee_work():
    times = request.json
    print(times)
    print(type(times))
    print("reach here")
    token = request.headers.get("X-Auth-Token")
    auth = jwt.decode(token, app.config['SECRET_KEY'])
    results = service.time_for_employee(email=auth['user'], times=times)
    # print("type", type(data[0][3]))
    # print("string", data[0][0].__str__().parse())
    # return {"rows" : json.dumps(data[0][0].__str__())}
    print(results)
    return {"rows" : results}

@app.route("/employees", methods = ["GET"])
def get_list_employees():
    employees = service.get_employees()
    return {
        "rows" : employees
    }
@app.route("/admin/history", methods = ["POST"])
def admin_history():
    data = request.json
    print(data)
    id = data['id']
    data.pop('id')
    response =  service.see_particular_employee(id, data)
    print(response)
    return {"rows" : response}

if __name__ == "__main__" :
    CORS(app)
    app.run()
