import numpy as np
import cv2
import requests
import time
import base64
from io import BytesIO
from alignment.detector import Retinaface_Detector
face_detection=Retinaface_Detector(device=0)

def convert_to_b64(img):
    _, im_arr = cv2.imencode('.png', img)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    return str(im_b64)[2:-1]

cap = cv2.VideoCapture("http://192.168.1.101:8080/video")
url = 'http://0.0.0.0:3007/'

t = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if t % 3 == 0 : 
        img_b64s=[]
        boxes,faces=face_detection.align_multi(frame)
        print(len(boxes))
        # Display the resulting frame
        if(len(boxes)>0):
            for face in faces:
                face = np.array(face)
                img_b64s.append(convert_to_b64(face))
            res = requests.post(url+"/attendance", json={"image":img_b64s})
            print(res.text)
    t += 1
    frame = cv2.resize(frame, (680, 460))
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
