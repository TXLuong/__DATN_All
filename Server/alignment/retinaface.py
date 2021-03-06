import os
import sys
import numpy as np
import cv2
import torch
from torch.autograd import Variable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from retinaface_pytorch.retinaface import load_retinaface_mbnet, RetinaFace_MobileNet
from retinaface_pytorch.utils import RetinaFace_Utils
from retinaface_pytorch.align_trans import get_reference_facial_points, warp_and_crop_face
from torchvision import transforms as trans
def sort_list(list1): 
    z = [list1.index(x) for x in sorted(list1, reverse = True)] 
    return z 
class Retinaface_Detector(object):
    def __init__(self, device = torch.device("cuda"), thresh = 0.6, atrib = True,  scales = [240, 320]):
        self.target_size = scales[0]
        self.max_size = scales[1]
        self.threshold = thresh
        if device:
            # assert device in
            self.device = device
        else:
            self.device = torch.device("cuda")

        self.model = RetinaFace_MobileNet()
        self.model = self.model.to(self.device)
        checkpoint = torch.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'retinaface_pytorch/checkpoint_1.pth'))
        self.model.load_state_dict(checkpoint['state_dict'])
        del checkpoint

        self.model.eval()
        self.pixel_means = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.pixel_stds = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        self.pixel_scale = float(1.0)
        self.refrence = get_reference_facial_points(default_square= True)
        self.utils = RetinaFace_Utils()

    def align(self, img, limit = None, min_face_size=None, thresholds = None, nms_thresholds=None):
        dict_output = self.align_multi(img)
        if len(dict_output['faces']) > 0:
            return dict_output["bboxs"][0], dict_output['faces'][0]
        return None, None

    def align_multi(self, img, limit = None, min_face_size=None, thresholds = None, nms_thresholds=None):
        faces = []
        faces_2_tensor = []
        img = np.array(img)
        im, im_scale = self.img_process(img)
        im = torch.from_numpy(im)
        im_tensor = Variable(im).to(self.device)
        output = self.model(im_tensor)
        sort = True
        boxes, landmarks = self.utils.detect(im, output, self.threshold, im_scale)          

        if limit:
            boxes, landmarks = boxes[:limit], landmarks[:limit]  

        boxes = boxes.astype(np.int)
        landmarks = landmarks.astype(np.int)
        face_area = (boxes[:,2] - boxes[:,0])*(boxes[:,3]-boxes[:, 1])
        if len(boxes) > 0 and sort:
            face_area = (boxes[:,2] - boxes[:,0])*(boxes[:,3]-boxes[:, 1])
            indexs = np.argsort(face_area)[::-1]
            boxes = boxes[indexs]
            landmarks = landmarks[indexs]
            for i, landmark in enumerate(landmarks):
                warped_face, face_img_tranform = warp_and_crop_face(img, landmark, self.refrence, crop_size=(112,112))
                warped_face = cv2.cvtColor(warped_face, cv2.COLOR_BGR2RGB) 
                face = Image.fromarray(warped_face)
                faces.append(face)
        return boxes,faces

    def img_process(self, img):
        im_shape = img.shape
        im_size_min = np.min(im_shape[0:2])
        im_size_max = np.max(im_shape[0:2])
        im_scale = float(self.target_size) / float(im_size_min)
        if np.round(im_scale * im_size_max) > self.max_size:
            im_scale = float(self.max_size) / float(im_size_max)
        im = cv2.resize(img, None, None, fx=im_scale, fy=im_scale, interpolation=cv2.INTER_LINEAR)
        # im = im.astype(np.float32)

        im_tensor = np.zeros((1, 3, im.shape[0], im.shape[1]), dtype=np.float32)
        for i in range(3):
            im_tensor[0, i, :, :] = (im[:, :, 2 - i] / self.pixel_scale - self.pixel_means[2 - i])/self.pixel_stds[2 - i]
        return im_tensor, im_scale



import time
if __name__ == '__main__':
    reti = Retinaface_Detector()
    img = cv2.imread("t2.jpg")
    t = time.time()
    for i in range(10):
        bboxs, faces = reti.align_multi(img)
        t2 = time.time()
        print(t2 -t)
        t = t2
    i=0
    for face in faces:
        i+=1
        face.save("a%d.jpg"%i)