
from  utils.utils import  *
from classification_test import *
import random
videList = getVideosList('C:/Users/kuba/Desktop/script/downloadedYT','.mp4')
print(videList)

classLists=[[],[],[]]

for video in videList:
    videoNumber = video[48:-6]
    videoClass= video[-5:-4]

    if(videoClass=='A'):
        classLists[0].append(int(videoNumber))
    if(videoClass=='B'):
        classLists[1].append(int(videoNumber))
    if(videoClass=='C'):
        classLists[2].append(int(videoNumber))

results=[]
for i in range(0,6):
    random.shuffle(classLists[0])
    random.shuffle(classLists[1])
    random.shuffle(classLists[2])
    print("iteracja numer "+ str(i))
    class_list = ['class_1', 'class_2', 'class_3']
    trainingLists = [classLists[0][0:10], classLists[1][0:10], classLists[2][0:3]]

    for single_class in class_list:
        print(class_list)
        model = train_model(single_class,trainingLists)
        joblib.dump(model, "models/model_for_" + single_class + ".pkl")

    results.append(classify_videos(trainingLists,30))

max=[]
maxValue=0
maxIndeks=0
i=0
for element in results:
    if(element[0]>maxValue):
        maxValue=element[0]
        max=element
    i=i+1
print (results)
print(max)