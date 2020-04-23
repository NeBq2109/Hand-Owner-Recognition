from cv2 import cv2 #openCV
import hand_func as piw
import numpy as np #array objects etc
import math
from matplotlib import pyplot as plt
import sys, os         
pathname = os.path.dirname(sys.argv[0])        
path=os.path.abspath(pathname)+'\\images'

lista_imion=[]
z=open("WyniczkiTakie.txt", "a+")
for iterator in range(15,16):
    i=0
    index='A'
    k=1
    if i==1: # i=1 zapi
        f=open("daneNowe.txt", "a+")
    if iterator<5: znak=r'\A'+str(iterator%5+1)+'.jpg'
    if iterator>=5 and iterator<10:  znak=r'\K'+str(iterator%5+1)+'.jpg'
    if iterator>=10 and iterator<15:  znak=r'\T'+str(iterator%5+1)+'.jpg'
    if iterator>=15 and iterator<20:  znak=r'\M'+str(iterator%5+1)+'.jpg'
    if iterator>=20 and iterator<25:  znak=r'\H'+str(iterator%5+1)+'.jpg'
    if iterator>=25 and iterator<30:  znak=r'\W'+str(iterator%5+1)+'.jpg'
    if iterator>=30 and iterator<35:  znak=r'\B'+str(iterator%5+1)+'.jpg'
    if iterator>=35:  znak=r'\C'+str(iterator%5+1)+'.jpg'
    path+=znak
    print(path)
    # Image read
    image = cv2.imread(path)
    original = image
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Detect skin areas from the image and create B&W image
    BinaryImage=piw.skin_extract(image)
    #cv2.imshow('Binary',BinaryImage)
    # Find the biggest contour
    largest_contour=piw.FB_contours(BinaryImage)
    # Get the angle
    #_,_,angle = cv2.fitEllipse(largest_contour)

    # Get position of hand region from the image
    x,y,width,height = cv2.boundingRect(largest_contour)
    # Extract hand part from the image.
    final_image = BinaryImage[y:y+height,x:x+width]
    hand_before_cut=final_image

    #final_image,final_row=piw.wrist_cut(final_image,width)
    # draw polygon
    largest_contour=piw.FB_contours(final_image)
    x,y,width,height = cv2.boundingRect(largest_contour)
    drawing,pointlist=piw.contour_points(largest_contour,image)
    print(pointlist)
    #cv2.circle(drawing,pointlist[6],5,[255,0,255],-1)
    # print images


    ratios=piw.calculateRatios(pointlist)
    print('ratios=',ratios)

    str_output=piw.ownerChoice(ratios)
    print(str_output)
    cv2.imwrite('contour.jpg',drawing[:y+height,:x+width])
    #str_output='nic'
    plt.subplot(1,3,1),plt.imshow(cv2.cvtColor(original,cv2.COLOR_BGR2RGB))
    plt.title('Original')
    plt.xticks([]),plt.yticks([])
    plt.subplot(1,3,3),plt.imshow(cv2.cvtColor(drawing[:y+height,:x+width],cv2.COLOR_BGR2RGB))
    plt.title('Contour with points')
    plt.xticks([]),plt.yticks([])
    plt.subplot(1,3,2),plt.imshow(cv2.cvtColor(final_image,cv2.COLOR_BGR2RGB))
    plt.title('Binarized hand')
    plt.xticks([]),plt.yticks([])
    plt.suptitle(str_output, fontsize=16)
    if k==1: plt.show()


    lista_imion.append(str_output)
    if i==1:
        f.write("\n%s %f %f %f %f %f" %(index,ratios[0],ratios[1],ratios[2],ratios[3],ratios[4]))
        f.close()

for item in lista_imion:
    z.write("%s\n" % item)
