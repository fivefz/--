# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 21:27:09 2019

@author: xiaoyifu
"""

import os
import urllib
import torch
import torch.nn as nn
import torch.nn.functional as F
 
#import torch.utils.model_zoo as model_zoo
from torchvision import models
#https://raw.githubusercontent.com/delta-onera/delta_tb/master/deltatb/networks/net_segnet_bn_relu.py
class SegNet_BN_ReLU(nn.Module):
    # Unet network
    @staticmethod
    def weight_init(m):
        if isinstance(m, nn.Linear):
            torch.nn.init.kaiming_normal(m.weight.data)
     
    def __init__(self, in_channels, out_channels):
        super(SegNet_BN_ReLU, self).__init__()
 
        self.in_channels = in_channels
        self.out_channels = out_channels
 
        self.pool = nn.MaxPool2d(2, return_indices=True)
        self.unpool = nn.MaxUnpool2d(2)
         
        self.conv1_1 = nn.Conv2d(in_channels, 64, 3, padding=1)
        self.conv1_1_bn = nn.BatchNorm2d(64)
        self.conv1_2 = nn.Conv2d(64, 64, 3, padding=1)
        self.conv1_2_bn = nn.BatchNorm2d(64)
         
        self.conv2_1 = nn.Conv2d(64, 128, 3, padding=1)
        self.conv2_1_bn = nn.BatchNorm2d(128)
        self.conv2_2 = nn.Conv2d(128, 128, 3, padding=1)
        self.conv2_2_bn = nn.BatchNorm2d(128)
         
        self.conv3_1 = nn.Conv2d(128, 256, 3, padding=1)
        self.conv3_1_bn = nn.BatchNorm2d(256)
        self.conv3_2 = nn.Conv2d(256, 256, 3, padding=1)
        self.conv3_2_bn = nn.BatchNorm2d(256)
        self.conv3_3 = nn.Conv2d(256, 256, 3, padding=1)
        self.conv3_3_bn = nn.BatchNorm2d(256)
         
        self.conv4_1 = nn.Conv2d(256, 512, 3, padding=1)
        self.conv4_1_bn = nn.BatchNorm2d(512)
        self.conv4_2 = nn.Conv2d(512, 512, 3, padding=1)
        self.conv4_2_bn = nn.BatchNorm2d(512)
        self.conv4_3 = nn.Conv2d(512, 512, 3, padding=1)
        self.conv4_3_bn = nn.BatchNorm2d(512)
         
        self.conv5_1 = nn.Conv2d(512, 512, 3, padding=1)
        self.conv5_1_bn = nn.BatchNorm2d(512)
        self.conv5_2 = nn.Conv2d(512, 512, 3, padding=1)
        self.conv5_2_bn = nn.BatchNorm2d(512)
        self.conv5_3 = nn.Conv2d(512, 512, 3, padding=1)
        self.conv5_3_bn = nn.BatchNorm2d(512)
         
        self.conv5_3_D = nn.Conv2d(512, 512, 3, padding=1)
        self.conv5_3_D_bn = nn.BatchNorm2d(512)
        self.conv5_2_D = nn.Conv2d(512, 512, 3, padding=1)
        self.conv5_2_D_bn = nn.BatchNorm2d(512)
        self.conv5_1_D = nn.Conv2d(512, 512, 3, padding=1)
        self.conv5_1_D_bn = nn.BatchNorm2d(512)
         
        self.conv4_3_D = nn.Conv2d(512, 512, 3, padding=1)
        self.conv4_3_D_bn = nn.BatchNorm2d(512)
        self.conv4_2_D = nn.Conv2d(512, 512, 3, padding=1)
        self.conv4_2_D_bn = nn.BatchNorm2d(512)
        self.conv4_1_D = nn.Conv2d(512, 256, 3, padding=1)
        self.conv4_1_D_bn = nn.BatchNorm2d(256)
         
        self.conv3_3_D = nn.Conv2d(256, 256, 3, padding=1)
        self.conv3_3_D_bn = nn.BatchNorm2d(256)
        self.conv3_2_D = nn.Conv2d(256, 256, 3, padding=1)
        self.conv3_2_D_bn = nn.BatchNorm2d(256)
        self.conv3_1_D = nn.Conv2d(256, 128, 3, padding=1)
        self.conv3_1_D_bn = nn.BatchNorm2d(128)
         
        self.conv2_2_D = nn.Conv2d(128, 128, 3, padding=1)
        self.conv2_2_D_bn = nn.BatchNorm2d(128)
        self.conv2_1_D = nn.Conv2d(128, 64, 3, padding=1)
        self.conv2_1_D_bn = nn.BatchNorm2d(64)
         
        self.conv1_2_D = nn.Conv2d(64, 64, 3, padding=1)
        self.conv1_2_D_bn = nn.BatchNorm2d(64)
        self.conv1_1_D = nn.Conv2d(64, out_channels, 3, padding=1)
         
        self.apply(self.weight_init)
         
    def forward(self, x):
        # Encoder block 1
        x =F.avg_pool2d(x,4)
        #print(x.shape)
        x = self.conv1_1_bn(F.relu(self.conv1_1(x)))
        x1 = self.conv1_2_bn(F.relu(self.conv1_2(x)))
        size1 = x.size()
        x, mask1 = self.pool(x1)
         
        # Encoder block 2
        x = self.conv2_1_bn(F.relu(self.conv2_1(x)))
        #x = self.drop2_1(x)
        x2 = self.conv2_2_bn(F.relu(self.conv2_2(x)))
        size2 = x.size()
        x, mask2 = self.pool(x2)
         
        # Encoder block 3
        x = self.conv3_1_bn(F.relu(self.conv3_1(x)))
        x = self.conv3_2_bn(F.relu(self.conv3_2(x)))
        x3 = self.conv3_3_bn(F.relu(self.conv3_3(x)))
        size3 = x.size()
        x, mask3 = self.pool(x3)
         
        # Encoder block 4
        x = self.conv4_1_bn(F.relu(self.conv4_1(x)))
        x = self.conv4_2_bn(F.relu(self.conv4_2(x)))
        x4 = self.conv4_3_bn(F.relu(self.conv4_3(x)))
        size4 = x.size()
        x, mask4 = self.pool(x4)
         
        # Encoder block 5
        x = self.conv5_1_bn(F.relu(self.conv5_1(x)))
        x = self.conv5_2_bn(F.relu(self.conv5_2(x)))
        x = self.conv5_3_bn(F.relu(self.conv5_3(x)))
        size5 = x.size()
        x, mask5 = self.pool(x)
         
        # Decoder block 5
        x = self.unpool(x, mask5, output_size = size5)
        x = self.conv5_3_D_bn(F.relu(self.conv5_3_D(x)))
        x = self.conv5_2_D_bn(F.relu(self.conv5_2_D(x)))
        x = self.conv5_1_D_bn(F.relu(self.conv5_1_D(x)))
         
        # Decoder block 4
        x = self.unpool(x, mask4, output_size = size4)
        x = self.conv4_3_D_bn(F.relu(self.conv4_3_D(x)))
        x = self.conv4_2_D_bn(F.relu(self.conv4_2_D(x)))
        x = self.conv4_1_D_bn(F.relu(self.conv4_1_D(x)))
         
        # Decoder block 3
        x = self.unpool(x, mask3, output_size = size3)
        x = self.conv3_3_D_bn(F.relu(self.conv3_3_D(x)))
        x = self.conv3_2_D_bn(F.relu(self.conv3_2_D(x)))
        x = self.conv3_1_D_bn(F.relu(self.conv3_1_D(x)))
         
        # Decoder block 2
        x = self.unpool(x, mask2, output_size = size2)
        x = self.conv2_2_D_bn(F.relu(self.conv2_2_D(x)))
        x = self.conv2_1_D_bn(F.relu(self.conv2_1_D(x)))
         
        # Decoder block 1
        x = self.unpool(x, mask1, output_size = size1)
        x = self.conv1_2_D_bn(F.relu(self.conv1_2_D(x)))
        x = self.conv1_1_D(x)
        #print(x.shape)
        return F.interpolate(x,mode='bilinear',scale_factor=4) 
 
    def load_pretrained_weights(self):
 
        #vgg16_weights = model_zoo.load_url("https://download.pytorch.org/models/vgg16_bn-6c64b313.pth")
        vgg16_weights=models.vgg16_bn(True).state_dict()
        count_vgg = 0
        count_this = 0
 
        vggkeys = list(vgg16_weights.keys())
        thiskeys  = list(self.state_dict().keys())
 
        corresp_map = []
 
        while(True):
            vggkey = vggkeys[count_vgg]
            thiskey = thiskeys[count_this]
 
            if "classifier" in vggkey:
                break
             
            while vggkey.split(".")[-1] not in thiskey:
                count_this += 1
                thiskey = thiskeys[count_this]
 
 
            corresp_map.append([vggkey, thiskey])
            count_vgg+=1
            count_this += 1
 
        mapped_weights = self.state_dict()
        for k_vgg, k_segnet in corresp_map:
            if (self.in_channels != 3) and "features" in k_vgg and "conv1_1." not in k_segnet:
                mapped_weights[k_segnet] = vgg16_weights[k_vgg]
            elif (self.in_channels == 3) and "features" in k_vgg:
                mapped_weights[k_segnet] = vgg16_weights[k_vgg]
 
        try:
            self.load_state_dict(mapped_weights)
            print("Loaded VGG-16 weights in Segnet !")
        except:
            print("Error VGG-16 weights in Segnet !")
            raise
     
    def load_from_filename(self, model_path):
        """Load weights from filename."""
        th = torch.load(model_path)  # load the weigths
        self.load_state_dict(th)
 
 
def segnet_bn_relu(in_channels, out_channels, pretrained=False, **kwargs):
    """Constructs a ResNet-34 model.
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    model = SegNet_BN_ReLU(in_channels, out_channels)
    if pretrained:
        model.load_pretrained_weights()
    return model
 
if __name__=='__main__':
    net=segnet_bn_relu(3,4,False)
    print(net)
    x=torch.rand((1,3,1024,1024))
    print(net.forward(x).shape)