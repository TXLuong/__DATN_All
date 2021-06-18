import torch
from PIL import Image
import cv2
import torch.nn.functional as F
import numpy as np
from torchvision.models.resnet import BasicBlock
from torchvision.models.resnet import ResNet
import torch.nn as nn
from torchvision import datasets, models, transforms
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
path_cur=os.path.dirname(os.path.abspath(__file__))

class Face_mask:
    def __init__(self,device=torch.device("cuda")):
        self.device=device
        self.output_dim=2
        self.input_size=112
        self.transform = transforms.Compose([
                transforms.Resize((self.input_size, self.input_size)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
        self.load_model()
        self.class_name=["Yes","No"]
    def create_resnet9_model(self):
        model = ResNet(BasicBlock, [1, 1, 1, 1])
        in_features = model.fc.in_features
        model.avgpool = nn.AdaptiveAvgPool2d(1)
        model.fc = nn.Linear(in_features, self.output_dim)
        return model
    def load_model(self):
        self.model = self.create_resnet9_model()
        self.model.to(self.device)
        self.model.load_state_dict(torch.load(os.path.join("face/weights",'face_mask_res9.pth'),  map_location="cuda" if torch.cuda.is_available() else "cpu"))
        self.model.eval()
    def predict_sigle(self,image): #image PIL
        img_torch=self.transform(image)
        img_torch=img_torch.unsqueeze(0)
        output=F.softmax(self.model(img_torch.to(self.device)))
        return output[0].cpu().detach().numpy(),self.class_name[int(output.argmax(1))],float(torch.max(output))

if __name__ == '__main__':
    X = Face_mask()
    img=Image.open("test.jpg").convert("RGB")
    print(X.predict_sigle(img))
