from cv2 import cv2
import numpy as np
import math
import sys, os         




def FB_contours(image):
    contours,_ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    length = len(contours)
    max_area = -1
    ci=0
    if length > 0:
        for i in range(length):
            temp = contours[i]
            area = cv2.contourArea(temp)
        if area > max_area:
            max_area = area
            ci = i
        maxContour=contours[ci]
    return maxContour

def skin_extract(image):

    img_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #skin color range for hsv color space 
    HSV_mask = cv2.inRange(img_HSV, (0, 15, 0), (17,170,255))
    #cv2.imshow('HSV mask_before',HSV_mask)
    #cv2.imwrite('HSV mask_before.jpg',HSV_mask)
    HSV_mask = cv2.morphologyEx(HSV_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    #cv2.imshow('HSV mask',HSV_mask)
    #cv2.imwrite('HSV mask.jpg',HSV_mask)
    #converting from gbr to YCbCr color space
    img_YCrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    #skin color range for hsv color space 
    YCrCb_mask = cv2.inRange(img_YCrCb, (0, 135, 85), (255,180,135)) 
    #cv2.imshow('YCrCb_mask_before',YCrCb_mask)
    #cv2.imwrite('YCrCb_mask_before.jpg',YCrCb_mask)
    YCrCb_mask = cv2.morphologyEx(YCrCb_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    #cv2.imshow('YCrCb_mask',YCrCb_mask)
    #cv2.imwrite('YCrCb_mask.jpg',YCrCb_mask)

    #merge skin detection (YCbCr and hsv)
    global_mask=cv2.bitwise_and(YCrCb_mask,HSV_mask)
    #cv2.imshow('global_mask_before',YCrCb_mask)
    cv2.imwrite('global_mask_befores.jpg',YCrCb_mask)
    global_mask=cv2.medianBlur(global_mask,3)
    global_mask = cv2.morphologyEx(global_mask, cv2.MORPH_OPEN, np.ones((4,4), np.uint8))
    #cv2.imshow('global_mask',YCrCb_mask)
    cv2.imwrite('global_mask.jpg',YCrCb_mask)

    return YCrCb_mask

def wrist_cut(final_image,width):
    temp = final_image.tolist()
    n = len(temp)

    # get rid off edges and slides due to previous rotate operation
    min_count, final_row, prev_count = width, 0, 0
    i=n-1
    for i in range(n-1,int(n/2),-1):
        count=int(sum(temp[i])/255)
        if count<prev_count:
            start = i
            break
        prev_count = count

    for i in range(start,int(n/3),-1):
        count=int(sum(temp[i])/255)
        if count<=min_count:
            final_row = i+1
            min_count=count

    # Extract the hand part and remove the arm part
    final_image = final_image[:final_row,:]

    return final_image,final_row

def contour_points(largest_contour,image):
    hull = cv2.convexHull(largest_contour)
    drawing = np.zeros(image.shape, np.uint8)
    cv2.drawContours(drawing, [largest_contour], 0, (0, 255, 0), 2)
    #cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)
    hull = cv2.convexHull(largest_contour,returnPoints = False)
    defects = cv2.convexityDefects(largest_contour,hull)
    # draw furthest left,top and right point
    point_list=[]
    # detect fingers middle defects
    k=1
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(largest_contour[s][0])
        end = tuple(largest_contour[e][0])
        far = tuple(largest_contour[f][0])
        angle = calculateAngle(far, start, end)
        if d > 10000 and angle <= math.pi/2:
            if(k==1):
                cv2.circle(drawing, start, 8, (147, 20, 255), -1)
                point_list.append(start)
            cv2.circle(drawing, end, 8, (147, 20, 255), -1)
            point_list.append(far)
            point_list.append(end)
            cv2.circle(drawing,far,5,[255,0,0],-1)
            k+=1

            
    return drawing,point_list

def calculateAngle(far, start, end):
    a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
    c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
    angle = math.acos((b**2 + c**2 - a**2) / (2*b*c))
    return angle

def calculateRatios(p):

    d1=getDistance(p[0],p[1])
    d2=getDistance(p[2],p[3])
    d3=getDistance(p[3],p[4])
    d4=getDistance(p[5],p[6])
    d5=getDistance(p[7],p[8])
    d6=getDistance(p[1],p[2])
    t1=getDistance(p[5],p[7])
    t2=getDistance(p[5],p[3])
    ratios=[d5/d4,d4/d3,d3/t2,d2/t1,d6/d1]
    return ratios

def heron(a,b,c):
    s = (a + b + c) / 2
    # calculate the area
    area = (s*(s-a)*(s-b)*(s-c)) ** 0.5
    return area

def getDistance(point1,point2):

    distance=math.sqrt((point1[1]-point2[1])**2+(point1[0]-point2[0])**2)
    return distance

def ownerChoice(ratios):
    pathname = os.path.dirname(sys.argv[0])        
    path=os.path.abspath(pathname)+ '\\\daneNowe.txt'
    file = open(path, 'r')
    k=-1
    myList=[[0,'Albert'],[1,'Krystian'],[2,'Tomasz'],[3,'Mateusz'],[4,'Henryk'],[5,'Weronika']]
    '''
    sum1=np.zeros(6)
    sum2=np.zeros(6)
    sum3=np.zeros(6)
    sum4=np.zeros(6)
    sum5=np.zeros(6)
    '''
    sum=np.zeros(6)
    quantity=np.copy(sum)
    decider=np.copy(sum)
    previousCell='X'
    for line in file.readlines():
        currentCell = line.rstrip().split(' ')
        
        if previousCell[0]!=currentCell[0]:
            k=k+1
        
        sum[k]=sum[k]+math.sqrt(
        (ratios[0]-float(currentCell[1]))**2+
        (ratios[1]-float(currentCell[2]))**2
        +(ratios[2]-float(currentCell[3]))**2
        +(ratios[3]-float(currentCell[4]))**2
        +(ratios[4]-float(currentCell[5]))**2
        )
        quantity[k]+=1
        previousCell=currentCell[0]
    
    decider=np.divide(sum,quantity)
    print(decider)
    print(quantity)
    mymin = np.min(decider)
    min_p = [i for i, x in enumerate(decider) if x == mymin]    
    for i in range(k+1):
        if min_p[0]==myList[i][0]:
            break
    
    str_output="This hand belongs to: "
    if mymin<0.35:
        str_output+=myList[i][1]
    else:
        str_output+='noone'
    return str_output