
from train.model_training import *
# news talshow reportaz wywiad reportaz wywiad talkshow
def classify_videos (trainingLists,obLenght):
    trainingList=[]
    for i in range(0,len(trainingLists) ):
        trainingList.extend(trainingLists[i])



    video_observation_list=[]
    for i in range(0,7):
        video_observation_list.append('test_data/sequences_video_' + str(i)+ '.txt')
    for i in range(8,29):
        video_observation_list.append('test_data/sequences_video_' + str(i) + '.txt')
    for i in range(30, 43):
         video_observation_list.append('test_data/sequences_video_' + str(i) + '.txt')
    for i in range(44, 88):
         video_observation_list.append('test_data/sequences_video_' + str(i) + '.txt')
    for i in range(89, 106):
         video_observation_list.append('test_data/sequences_video_' + str(i) + '.txt')

    class_list = ['class_1', 'class_2', 'class_3']
    class_names = {class_list[0]:"A", class_list[1]:"B", class_list[2]:"C"}
    wynik=''
    classification_results = {}

    for video_data_path in video_observation_list:
        # print(video_data_path)
        observation=joblib.load(video_data_path)
        data = Counter(observation)

        print(video_data_path + ' '+ str(observation))
        print("CZĘSTOTLIWOSCI")
        for a in data.most_common():
            desc=Observation(int(a[0][0]),bool(a[0][1]),bool(a[0][2]),int(a[0][3]),bool(a[0][4]))

            print(str(desc) + " " + str(a[1]))





        if len(observation) >obLenght:
            observation = observation[0:obLenght]

        # print(observation)

        wynik=wynik+('\n'+"Plik testowy "+video_data_path+'\n')
        scores={}


        for single_class in class_list :
            model= joblib.load("models/model_for_"+single_class+".pkl")
            score=model.score(observation)
            scores[single_class]=score

            correction=''
            if single_class=='class_3' and score>0 and (scores['class_1']+scores['class_2'])/score <3  :
                score=scores['class_1']+scores['class_2']
                scores['class_3'] = score




            wynik=wynik+" dla klasy " + class_names[single_class] + " wynik to " + str(score)+'\n'
        predicted_class=''
        for key, value in scores.items():
            if value==max(list(scores.values())) :
                predicted_class=key
        classification_results[video_data_path]=predicted_class

    print(wynik)
    #print(classification_results)
    predictedMap={}
    for key , value in classification_results.items():
        # print ( key[26:-4] +","+class_names[value])
        predictedMap[key[26:-4]]=class_names[value]

    videList = getVideosList('C:/Users/kuba/Desktop/script/downloadedYT','.mp4')
    # print(videList)

    properMap = {}
    for video in videList:
        videoNumber = video[48:-6]
        videoClass= video[-5:-4]
        # print(videoNumber + ' ' + videoClass)
        properMap[videoNumber]=videoClass

    allA=0
    allB=0
    allC=0

    trainingList = list(map(int, trainingList))


    for key , value in properMap.items():
        if True:
            if value=='A':
                allA+=1
            if value=='B':
                allB+=1
            if value=='C':
                allC+=1

    allTestVideo=0
    recognizednumber=0
    recognizednumberA=0
    recognizednumberB=0
    recognizednumberC=0
    for key , value in predictedMap.items():
        if True:
            allTestVideo+=1
            if properMap[key]==value:
                recognizednumber+=1
                if value == 'A':
                    recognizednumberA += 1
                if value == 'B':
                    recognizednumberB += 1
                if value == 'C':
                    recognizednumberC += 1

    for key , value in predictedMap.items():
        if int(key) not in trainingList:

            print( "video" + key + "  "+ properMap[key] + " "+predictedMap[key] )
        else:
            print("video" + key + "  " + properMap[key] + " " + predictedMap[key] + "     training")

    print("skuteczność to  "+str(recognizednumber) +'/' + str(allTestVideo) + '='+str(recognizednumber/allTestVideo))
    print("skuteczność A to "+str(recognizednumberA) +'/' + str(allA) + '=' +str(recognizednumberA/allA))
    print("skuteczność B to "+str(recognizednumberB) +'/' + str(allB) + '=' +str(recognizednumberB/allB))
    print("skuteczność C to "+str(recognizednumberC) +'/' + str(allC) + '=' +str(recognizednumberC/allC))

    toReturn= str(trainingLists) + '\n'
    toReturn+="skuteczność to  "+str(recognizednumber) +'/' + str(allTestVideo) + '='+str(recognizednumber/allTestVideo)+ '\n'
    toReturn+="skuteczność A to "+str(recognizednumberA) +'/' + str(allA) + '=' +str(recognizednumberA/allA)+ '\n'
    toReturn+="skuteczność B to "+str(recognizednumberB) +'/' + str(allB) + '=' +str(recognizednumberB/allB)+ '\n'
    toReturn+="skuteczność C to "+str(recognizednumberC) +'/' + str(allC) + '=' +str(recognizednumberC/allC)+ '\n'
    print(trainingList)

    #for class A
    return [recognizednumber/allTestVideo,toReturn]

#trainingList=[[0, 57, 13, 53, 58, 12, 16, 19, 89], [91, 69, 33, 26, 30, 37, 102], [38, 82, 81]]
trainingList=[[31, 4, 39, 51, 21, 10], [98, 70, 5, 105, 69, 28], [87, 82, 83]]


class_list = ['class_1', 'class_2', 'class_3']

for single_class in class_list:
    #print(class_list)
    model = train_model(single_class, trainingList)
    joblib.dump(model, "models/model_for_" + single_class + ".pkl")


string=classify_videos(trainingList,33)
print(string)
