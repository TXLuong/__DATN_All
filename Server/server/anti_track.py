import core as corelib
from efficientnet_pytorch import EfficientNet
import torchvision.transforms as transforms
import torch
import albumentations as alt
from albumentations.pytorch import ToTensorV2 as ToTensor
from imutils.video import VideoStream
from PIL import Image
import numpy
import cv2
import argparse
import time


class Anti_smoofing_track:
    def __init__(self, device):

        self.device = device
        self.model = {}
        self.model['lgsc'] = corelib.LGSC(drop_ratio=0.4)
        checkpoint = torch.load("weights/lgsc_siw_pretrained.pth", map_location=lambda storage, loc: storage)
        new_dict = {}
        for key in  checkpoint['backbone'].keys():
            new_dict[key.replace("module.", "")] = checkpoint['backbone'][key]
        self.model['lgsc'].load_state_dict(new_dict)
        self.model['lgsc'].to(self.device)
        self.model['lgsc'].eval()   # core

        self.model['classtify'] = EfficientNet.from_name('efficientnet-b0', num_classes=2)
        checkpoint = torch.load("weights/Iter_035000_net.ckpt", map_location=lambda storage, loc: storage)
        # print(checkpoint.keys())
        self.model['classtify'].load_state_dict(checkpoint['net_state_dict'])
        self.model['classtify'].to(self.device)
        self.model['classtify'].eval()
        self.tranform = {}
        self.tranform["classtify"] = transforms.Compose([
            transforms.Resize((112, 112)),
            transforms.ToTensor(),  # range [0, 255] -> [0.0,1.0]
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # range [0.0, 1.0] -> [-1.0,1.0]
        ])

        self.tranform["lgsc"] = alt.Compose([alt.Resize(224, 224, p=1), alt.Normalize(), ToTensor()])
        # self.

    def predict(self, face):
        print("Predict")
        img = self.tranform["classtify"](face)
        print("img after transformed", img)
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        raw_logits = self.model['classtify'](img.to(self.device))
        raw_logits = torch.nn.functional.softmax(raw_logits)
        score, predict = torch.max(raw_logits.data, 1)
        if predict[0] == 1 and score[0] > 0.8:
            phase2 = self.tranform['lgsc'](image=numpy.array(face))['image'].unsqueeze(0)
            imgs_feat, clf_out = self.model['lgsc'](phase2.to(self.device))
            spoof_score = torch.mean(torch.abs(imgs_feat[-1])).item()
            if spoof_score < 0.0095:
                return score[0], spoof_score, 1
        return score[0], 1, 0