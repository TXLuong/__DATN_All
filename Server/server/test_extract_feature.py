from posix import listdir
from support_api import Process_api
import numpy as np
import cv2
import requests
import time
import base64
from anti_track import Anti_smoofing_track
from face.face_process import face_recognize
import torch
import os
import sys
from PIL import Image
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
face = face_recognize()
face_anti_smoofing = Anti_smoofing_track(device)
process_api = Process_api("recognize_mask", face, face_anti_smoofing)
def check_spoofing(path_to_img):
    # img = cv2.imread("../son.jpg")
    img = cv2.imread(path_to_img)
    _, im_arr = cv2.imencode('.png', img)
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    base64String = str(im_b64)[2:-1]
    image = process_api.img_from_base64(base64String)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(image)
    return process_api.check_smoofing(im_pil)
    # print("begin checking spoofing")
    # (im_pil.show)
    # print("check spoofing", process_api.check_smoofing(im_pil))
    # print(image)
    # print("type:")
    # print(image.shape)
    # print(type(image))
def extract_from_face(file):
    img = cv2.imread(file)
    _, im_arr = cv2.imencode('.png', img)
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    base64String = str(im_b64)[2:-1]
    image = process_api.img_from_base64(base64String)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(image)
    return process_api.face.features_from_faces([im_pil])

    
def extract_features(file):
    print(file)
    img = cv2.imread(file)
    _, im_arr = cv2.imencode('.png', img)
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    base64String = str(im_b64)[2:-1]
    image = process_api.img_from_base64(base64String)
    feature = (process_api.get_feature(image))
    # print(type(feature))
    # print(feature.shape)
    # print(feature)
if __name__ == "__main__":
    path_resized = "/home/luong/datasets/data_resized/"
    list_dir_to_images = os.listdir(path_resized)
    print(len(list_dir_to_images))
    origins = []
    count = 0
    nums = 990

    for dir in list_dir_to_images : 
        if count > nums : 
            break
        list_file = os.listdir(path_resized + dir)
        feature = extract_from_face(path_resized+dir+"/"+list_file[0])
        feature = feature.tolist()
        origins.append(feature)
        count = count + 1
    count = nums
    predict = []
    khong_nhan_ra = 0
    results = [[0 for j in range(nums)] for i in range(nums)]
    print('-----------')
    for run in range(1,4):
        count = 0
        predict = []
        for dir in list_dir_to_images : 
            if count > nums : 
                break
            list_file = os.listdir(path_resized + dir)
            feature = extract_from_face(path_resized+dir+"/"+list_file[run])
            feature = feature.tolist()
            predict.append(feature)
            count = count + 1
        for i in range(nums):
            flag = True
            for j in range(nums):
                if process_api.recognize_for_report(origins[i], predict[j]):
                    results[i][j] = results[i][j] + 1
                    flag = False
            if flag :
                khong_nhan_ra = khong_nhan_ra + 1
    
                
    # so luong user A -> nhan ra user A 
    chiso1 = 0
    for i in range(nums):
        chiso1 = chiso1 + results[i][i]
    # so luong userA -> nhan ra user B
    chiso2 = 0
    for i in range(nums):
        chiso2 = chiso2 + sum(results[i]) - results[i][i]
    total = 0
    for i in range(nums):
        total = total + sum(results[i])
    print("sum : ", total)
    print("khong nhan ra ai ", khong_nhan_ra)
    # # so luong user A -> khong ra user nao 
    # chiso3 = 0
    # for i in range(nums):
    #     temp = False
    #     for j in range(nums):
    #         if results[i][j] != 0:
    #             temp = True
    #             break
    #     if temp == False:
    #         chiso3 = chiso3 +1
    print("chi so 1", chiso1)
    print("chi so 2", chiso2)
    # print("chi so 3", chiso3)
    print("do chinh xac acc ", chiso1/(3*nums + 0.0))
    so_luong_duoc = 0
    for i in range(nums):
        if results[i][i] > 0 : so_luong_duoc = so_luong_duoc +1
    print("so luong duoc : ", so_luong_duoc)

    