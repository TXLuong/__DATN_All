import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
path_cur=os.path.dirname(os.path.abspath(__file__)) 

import torch
import numpy as np
from PIL import Image
import cv2 
import math
import time
from torchvision import transforms
from backbones.iresnet import iresnet100
from alignment.detector import Retinaface_Detector
import torch.nn.functional as F
from face_mask import Face_mask
# from smoofing.Smoofing import Smoofing
class face_recognize(object):
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.setup()
        self.face_mask = Face_mask(self.device)
        
    def setup(self):
        self.limit=10
        self.use_tensor = False    #If False: su dung numpy dung cho tuong lai khi trien khai qua Product Quantizers cho he thong lon
    
        self.test_transform = transforms.Compose(
                                        [
                                        transforms.ToTensor(),
                                        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
                                        ])
        
        self.mtcnn = Retinaface_Detector(device = self.device, thresh = 0.4, scales = [360, 480])
        # self.anti_spoofing = Smoofing()
        self.tta = False
        self.min_face_size = 32.0
        self.load_model()

    def load_model(self):
        weight = torch.load(path_cur+"/weights/16_backbone.pth", map_location="cuda" if torch.cuda.is_available() else "cpu")
        resnet = iresnet100()
        resnet.load_state_dict(weight)
        self.model = torch.nn.DataParallel(resnet).to(self.device)
        self.model.eval()

    def check_face_mask(self, face) :
        face = face.convert("RGB")
        if self.face_mask.predict_sigle(face)[1] == 'No' :
            print("No Mask")
            return 0
        else :
            print("Mask")
            return 1
        
    def align_multi(self, img):
        bboxes, faces = self.mtcnn.align_multi(img, self.limit, self.min_face_size)
        return bboxes, faces

    def align(self,img):
        face = self.mtcnn.align(img)
        return face

    def feature_img(self, img):
        bboxes, faces  = self.align_multi(img)
        # bboxes, faces = dict_output["bboxs"], dict_output["faces"]
        
        embs = []
        for im in faces:
            embs.append(F.normalize(self.model(self.test_transform(im).to(self.device).unsqueeze(0))).data.cpu().numpy()[0])
        return np.array(embs), faces
    
    def feature_img_mask(self, img):
        bboxes, faces  = self.align_multi(img)
        # bboxes, faces = dict_output["bboxs"], dict_output["faces"]
        embs = []
        for im in faces:
            im = im.crop((0, 0, 112, 65)) 
            imn = Image.new(im.mode, (112, 112), (0,0,0))
            imn.paste(im, (0, 0))
            #imn.save("test.jpg")
            # im=im.resize((112,112))
            embs.append(F.normalize(self.model(self.test_transform(imn).to(self.device).unsqueeze(0))).data.cpu().numpy()[0])
        return np.array(embs), faces

    def features_from_faces(self,faces):
        embs = []
        for im in faces:
            embs.append(F.normalize(self.model(self.test_transform(im).to(self.device).unsqueeze(0))).data.cpu().numpy()[0])
        return np.array(embs)
    
    def features_from_faces_mask(self,faces):
        embs = []
        for im in faces:
            im = im.crop((0, 0, 112, 65)) 
            imn = Image.new(im.mode, (112, 112), (0,0,0))
            imn.paste(im, (0, 0))
            embs.append(F.normalize(self.model(self.test_transform(imn).to(self.device).unsqueeze(0))).data.cpu().numpy()[0])
        return np.array(embs)

    def feature_multi(self, img) :
        bboxes, faces  = self.align_multi(img)
        # bboxes, faces = dict_output["bboxs"], dict_output["faces"]
        embs = []
        embs2 = []

        for im in faces:
            im2 = im.crop((0, 0, 112, 65)) 
            imn = Image.new(im2.mode, (112, 112), (0,0,0))
            imn.paste(im2, (0, 0))
            embs.append(F.normalize(self.model(self.test_transform(im).to(self.device).unsqueeze(0))).data.cpu().numpy()[0])
            embs2.append(F.normalize(self.model(self.test_transform(imn).to(self.device).unsqueeze(0))).data.cpu().numpy()[0])

        return np.array(embs), np.array(embs2), faces

    
import cv2
import numpy as np
if __name__ == "__main__":
    face_model = face_recognize()
    # embs, faces = face.feature_img(cv2.imread("t2.jpg"))
    # print(embs.shape)
    img = cv2.imread("face/test.jpg")
    t = time.time()
    
    boxes, faces = face_model.align_multi(img)
    t2 = time.time()
    print(t2 - t)
    i = 0
    for box, face in zip(boxes, faces):
        box = box.astype(int)
        i += 1
        img_face = img[box[1] : box[3], box[0] : box[2], :]
        print(face_model.check_face_mask(face))
        face.save("face/" + str(i) + ".jpg")
        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 234, 123), 2)

    cv2.imwrite("face/result.jpg", img)
        
    
