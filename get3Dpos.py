'''
Author: SimonCK666 SimonYang223@163.com
Date: 2022-12-17 11:36:27
LastEditors: SimonCK666 SimonYang223@163.com
LastEditTime: 2022-12-17 11:39:12
FilePath: /Trangular_Depth_Estimation/get3Dpos.py
Reference: https://blog.csdn.net/summermaoz/article/details/103324287
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# To get the 3D position(X,Y,Z) from stereo images 
import os
import cv2
import xml.dom.minidom
from numpy import *
import numpy as np

def getInt_para(xmlfile):
	dom = xml.dom.minidom.parse(xmlfile)
	#得到文档元素对象
	root = dom.documentElement
	# ImageWidth = float(root.getElementsByTagName('Width')[0].childNodes[0].data)
	FocalLengthPixels = float(root.getElementsByTagName('FocalLengthPixels')[0].childNodes[0].data)
	# SensorSize = float(root.getElementsByTagName('SensorSize')[0].childNodes[0].data)
	# f = ImageWidth*FocalLength/SensorSize
	f = FocalLengthPixels
	PrincipalPoint = root.getElementsByTagName('PrincipalPoint')[0]
	x0 = float(PrincipalPoint.getElementsByTagName('x')[0].childNodes[0].data)
	y0 = float(PrincipalPoint.getElementsByTagName('y')[0].childNodes[0].data)
	# 相机内参
	K = mat([[f,0,x0],[0,f,y0],[0,0,1]]).reshape(3,3)
	return K, x0, y0

def getExt_para(xmlfile, imgname):
	dom = xml.dom.minidom.parse(xmlfile)
	#得到文档元素对象
	root = dom.documentElement
	ImagePathlist = root.getElementsByTagName('ImagePath')

	for i, Path in enumerate(ImagePathlist):
		ImagePath = Path.childNodes[0].data
		ImageName = ImagePath.split('\\')[-1]

		if ImageName == imgname:
			M_00 = float(root.getElementsByTagName('M_00')[i].childNodes[0].data)
			M_01 = float(root.getElementsByTagName('M_01')[i].childNodes[0].data)
			M_02 = float(root.getElementsByTagName('M_02')[i].childNodes[0].data)
			M_10 = float(root.getElementsByTagName('M_10')[i].childNodes[0].data)
			M_11 = float(root.getElementsByTagName('M_11')[i].childNodes[0].data)
			M_12 = float(root.getElementsByTagName('M_12')[i].childNodes[0].data)
			M_20 = float(root.getElementsByTagName('M_20')[i].childNodes[0].data)
			M_21 = float(root.getElementsByTagName('M_21')[i].childNodes[0].data)
			M_22 = float(root.getElementsByTagName('M_22')[i].childNodes[0].data)
			# 旋转矩阵
			R = mat([[M_00,M_01,M_02],[M_10,M_11,M_12],[M_20,M_21,M_22]]).reshape(3,3)

			x = float(root.getElementsByTagName('x')[i+1].childNodes[0].data)
			y = float(root.getElementsByTagName('y')[i+1].childNodes[0].data)
			z = float(root.getElementsByTagName('z')[i].childNodes[0].data)
			# 相机中心		
			C_center=mat([x,y,z]).reshape(3,1)
	return R, C_center

def calculate_3DX(kp1, kp2, Proj1, Proj2):
	A0 = mat(kp1[0] * Proj1[2,:] - Proj1[0,:])
	A1 = mat(kp1[1] * Proj1[2,:] - Proj1[1,:])
	A2 = mat(kp2[0] * Proj2[2,:] - Proj2[0,:])
	A3 = mat(kp2[1] * Proj2[2,:] - Proj2[1,:])
	train_data = mat(vstack((A0,A1,A2,A3)))
	U,sigma,VT = np.linalg.svd(train_data)
	posx = VT[3,:].T
	posx_ = posx / posx[3][0]
	position = posx_[0:3]
	return position

if __name__ == '__main__':
	# get camera intrinsic parameters K, C
	xmlfile = 'D:/experiments/TS-Reconstruct/Block_1 - AT -export.xml'
	imgname1 = 'DSC00041.jpg'
	imgname2 = 'DSC00044.jpg'
	K, x0, y0 = getInt_para(xmlfile)
	# get camera external parameters
	R1, C_center1 = getExt_para(xmlfile, imgname1)
	R2, C_center2 = getExt_para(xmlfile, imgname2)

	t1 = -R1 * C_center1
	t2 = -R2 * C_center2

	Proj1 = mat(K*hstack((R1,t1))) #投影矩阵P1
	Proj2 = mat(K*hstack((R2,t2))) #投影矩阵P2

	img_kp1 =(6672, 2716)
	img_kp2 =(6633, 2848)
	position = calculate_3DX(img_kp1, img_kp2, Proj1, Proj2)