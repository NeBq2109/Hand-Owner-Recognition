import numpy as np #array objects etc
import sys, os  

pathname = os.path.dirname(sys.argv[0])        
path=os.path.abspath(pathname)+ '\\dane.txt'

file = open(path, 'r')

k=-1
sum=[0,0,0,0,0,0,0,0]
previousCell='X'
dataSet=[]
for line in file.readlines():
    currentCell = line.rstrip().split(' ')
    dataSet.append(currentCell)
    if previousCell[0]!=currentCell[0]:
        k=k+1
    sum[k]=sum[k]+1   
    previousCell=currentCell[0]

print(dataSet[43][0])
a = np.array([1,2,3,1,2,1,1,1,3,2,2,1])
counts = np.bincount(a)
print(np.argmax(counts))