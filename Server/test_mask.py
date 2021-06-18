import numpy as np
import cv2
import requests
import time
import base64
def convert_to_b64(img):
    _, im_arr = cv2.imencode('.png', img)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    return str(im_b64)[2:-1]

url = 'http://45.122.253.30:3007'
image = cv2.imread("mask.jpg")
res = requests.post(url+"/test_face_mask", json={"image":convert_to_b64(image)}).text
print(res)

