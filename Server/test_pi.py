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

cap = cv2.VideoCapture("http://192.168.1.101:8080/video")
url = 'http://0.0.0.0:3007/'

t = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (720, 480))
    if t % 3 == 0 :
        res = requests.post(url+"attendance_pi", json={"image":convert_to_b64(frame)}).text
        print(res)
    t += 1
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
