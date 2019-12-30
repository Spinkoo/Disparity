import cv2
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import collections




"""


This generates a disparity map that goes as follow :
The brighter the pixel the closer to the camera 




"""
def distanceBasic(startlefti,startleftj,startrighti,startrightj,func):
	d=0
	b=blockRadius*2
	for i in range(0,b):
		for j in range(0,b):
			vall=imgleft[i+startlefti][startleftj+j]
			valr=imgright[i+startrighti][j+startrightj]
			d+=func(vall,valr)
	return d

def SSD(a,b):
	return ((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)**0.5
def AD(a,b):
	return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])
def CC(a,b):
	return a*b

def distanceNC(startlefti,startleftj,startrighti,startrightj):
	d=distanceBasic(imgleft,imgright,startlefti,startleftj,startrighti,startrightj,CC)
	return d**0.5
def rescale_linear(array, new_min=5, new_max=192):
    """Rescale an arrary linearly."""
    minimum, maximum = np.min(array), np.max(array)
    m = (new_max - new_min) / (maximum - minimum)
    b = new_min - m * minimum
    return m * array + b


#estimer l'espace de recherche d'apres le decalage initial 
def findbestMatch():
	matches=[]
	searchRadius=128
	for i in range (0,8):
		l=-searchRadius
		minIndex=0
		minim=99999

		while(l<searchRadius):
			d=distanceBasic(int(h/2)-blockRadius,int(w/2)+i-blockRadius,int(h/2)-blockRadius,int(w/2)+i-blockRadius+l,SSD)
			if(d<minim):
				minim=d
				minIndex=l
			if(minim<threshhold):
				break
			l+=1
		matches.append(minIndex)			
	negs=0
	pos=0
	return max(set(matches), key = matches.count) 










if(len(sys.argv)<3):
	print("too few arguemnts ( left and right images required  )")
	exit()


imgleft=cv2.imread(sys.argv[1],1)
imgright=cv2.imread(sys.argv[2],1)

imgleft=cv2.cvtColor(imgleft,cv2.COLOR_BGR2HSV)
imgright=cv2.cvtColor(imgright,cv2.COLOR_BGR2HSV)

imgleft=imgleft.astype(np.double)
imgright=imgright.astype(np.double)
 

h,w,_=np.shape(imgleft)
disparty=np.zeros((h,w),np.double)
searchRadius=16
blockRadius=4
threshhold=(blockRadius)**2

j=i=blockRadius
direction=findbestMatch()
end = searchRadius
while(i<h-blockRadius):
	j=blockRadius
	while(j<w-blockRadius):
		
		l=-searchRadius
		minIndex=0
		minim=99999
		while(l<end):
			if(direction+j+l>=blockRadius and direction+j+l<w-blockRadius):
				d=distanceBasic(i-blockRadius,j-blockRadius,i-blockRadius,direction+j-blockRadius+l,SSD)
				if(d<minim):
					minim=d
					minIndex=l+direction
			
					if(minim<threshhold):
							break
			l+=2
		minIndex=abs(minIndex)+searchRadius

		disparty[i][j]=(minIndex)
		m=i-2
		while m <i:
			n=j-2
			while n<j:
				disparty[m][n]=minIndex
				n+=1
			m+=1
		j+=2
	i+=2
disparty=disparty.astype(int)


#scale values to the range of a color [0:255]
disparty=rescale_linear(disparty)


#smooth the map

d=np.zeros((h,w,3),np.uint8)
for i in range (0,h):
	for j in range (0,w):
		val=disparty[i][j]
		d[i][j]=(val),(val),val

d=cv2.medianBlur(d,5)
d= cv2.bilateralFilter(d,9,75,75)
d=cv2.cvtColor(d, cv2.COLOR_BGR2GRAY ) 
cv2.imshow("disparity map",d)
cv2.waitKey(0)
cv2.imwrite("disparitymap.png",d)
