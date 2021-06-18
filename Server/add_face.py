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

data = {
    "name" : "Ngo Huu Son",
    "base64" : convert_to_b64(cv2.imread("son.jpg"))
}
url = 'http://0.0.0.0:3007/'
res = requests.post(url+"employee", json=data).text
print(res)
