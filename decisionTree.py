from sklearn import tree
from train.model_training import *
import graphviz
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/graphviz-2.38/release/bin'
# news talshow reportaz wywiad reportaz wywiad talkshow
def classify_videos():
    video_observation_list = []

    deciziontree = []
    classesForLearning=[]
    for i in range(0, 7):
        video_observation_list.append('test_data/sequences_video_' + str(i) + '.txt')
    for i in range(8, 29):
        video_observation_list.append('test_data/sequences_video_' + str(i) + '.txt')
    for i in range(30, 43):
        video_observation_list.append('test_data/sequences_video_' + str(i) + '.txt')
    for i in range(44, 88):
        video_observation_list.append('test_data/sequences_video_' + str(i) + '.txt')
    for i in range(89, 106):
        video_observation_list.append('test_data/sequences_video_' + str(i) + '.txt')

    class_list = ['class_1', 'class_2', 'class_3']
    class_names = {class_list[0]: "A", class_list[1]: "B", class_list[2]: "C"}
    wynik = ''
    classification_results = {}

    statisticList = {}
    statisticListA = {}
    statisticListB = {}

    countA = 0
    countB = 0
    countC = 0
    countD = 0
    countE = 0
    countF = 0

    for video_data_path in video_observation_list:
        # print(video_data_path)
        observation = joblib.load(video_data_path)
        data = Counter(observation)

        print(video_data_path + ' ' + str(observation))
        print("CZĘSTOTLIWOSCI")

        liczbaUjec = 0
        zNowymiOsobami = 0
        ZeStarymiOsobami = 0
        bezOsob = 0
        dwaUjecia = 0
        jednoUjecie = 0
        trzyLubWiecej = 0

        for a in data.most_common():
            desc = Observation(a[0][0], a[0][1], a[0][2], a[0][3], a[0][4])
            if (a[0][4]):
                liczbaUjec = liczbaUjec + a[1]
            if not (a[0][4]) and a[0][0] == 0:
                bezOsob = bezOsob + a[1]

            if not (a[0][4]) and a[0][0] != 0 and a[0][2]:
                ZeStarymiOsobami = ZeStarymiOsobami + a[1]
                if (a[0][2] == 1):
                    jednoUjecie = jednoUjecie + 1
                if (a[0][2] == 2):
                    dwaUjecia = dwaUjecia + 1
                else:
                    trzyLubWiecej = trzyLubWiecej + 1

            if not (a[0][4]) and a[0][0] != 0 and not a[0][2]:
                zNowymiOsobami = zNowymiOsobami + a[1]
            print(str(desc) + " " + str(a[1]))




        if (bezOsob / liczbaUjec > 0.9):
            classification_results[video_data_path] = "class_3"
            statisticList[video_data_path[26:-4]] = ()
        else:
            statisticList[video_data_path[26:-4]] = (
            zNowymiOsobami / (ZeStarymiOsobami + zNowymiOsobami), bezOsob / (ZeStarymiOsobami + zNowymiOsobami))

            if (ZeStarymiOsobami / (ZeStarymiOsobami + zNowymiOsobami) >= 0.9):
                classification_results[video_data_path] = "class_2"
                countA = countA + 1
            elif (zNowymiOsobami / (ZeStarymiOsobami + zNowymiOsobami) >= 0.6):
                classification_results[video_data_path] = "class_1"
                countB = countB + 1

            elif (ZeStarymiOsobami / (ZeStarymiOsobami + zNowymiOsobami)) >= 0.8 and dwaUjecia + jednoUjecie / (
                    dwaUjecia + jednoUjecie + trzyLubWiecej) > 0.4:
                classification_results[video_data_path] = "class_2"
                countC = countC + 1


            elif (bezOsob) / (ZeStarymiOsobami + zNowymiOsobami + bezOsob) >= 0.3:
                classification_results[video_data_path] = "class_1"
                countE = countE + 1

            else:
                countF = countF + 1

                classification_results[video_data_path] = "class_2"
        parametr1=bezOsob / liczbaUjec
        parametr2 = zNowymiOsobami / liczbaUjec
        parametr3 = ZeStarymiOsobami / liczbaUjec
        parametr4 = jednoUjecie / liczbaUjec
        parametr5 = dwaUjecia / liczbaUjec
        parametr6 = trzyLubWiecej / liczbaUjec

        deciziontree.append([parametr1,parametr2,parametr3,parametr4,parametr5,parametr6])
    print(wynik)
    # print(classification_results)
    predictedMap = {}
    for key, value in classification_results.items():
        # print ( key[26:-4] +","+class_names[value])
        predictedMap[key[26:-4]] = class_names[value]

    videList = getVideosList('C:/Users/kuba/Desktop/script/downloadedYT', '.mp4')
    # print(videList)

    properMap = {}
    for video in videList:
        videoNumber = video[48:-6]
        videoClass = video[-5:-4]
        # print(videoNumber + ' ' + videoClass)
        properMap[videoNumber] = videoClass

        if (videoClass == 'A'):
            statisticListA[videoNumber] = statisticList[videoNumber]
        if (videoClass == 'B' and videoNumber != str(29)):
            statisticListB[videoNumber] = statisticList[videoNumber]

    allA = 0
    allB = 0
    allC = 0

    for key, value in properMap.items():
        if True:
            if value == 'A':
                allA += 1
            if value == 'B':
                allB += 1
            if value == 'C':
                allC += 1

    allTestVideo = 0
    recognizednumber = 0
    recognizednumberA = 0
    recognizednumberB = 0
    recognizednumberC = 0
    for key, value in predictedMap.items():
        if True:
            allTestVideo += 1
            if properMap[key] == value:
                recognizednumber += 1
                if value == 'A':
                    recognizednumberA += 1
                if value == 'B':
                    recognizednumberB += 1
                if value == 'C':
                    recognizednumberC += 1

    for key, value in predictedMap.items():
        print("video" + key + "  " + properMap[key] + " " + predictedMap[key])
        classesForLearning.append(properMap[key])
    print("skuteczność to  " + str(recognizednumber) + '/' + str(allTestVideo) + '=' + str(
        recognizednumber / allTestVideo))
    print("skuteczność A to " + str(recognizednumberA) + '/' + str(allA) + '=' + str(recognizednumberA / allA))
    print("skuteczność B to " + str(recognizednumberB) + '/' + str(allB) + '=' + str(recognizednumberB / allB))
    print("skuteczność C to " + str(recognizednumberC) + '/' + str(allC) + '=' + str(recognizednumberC / allC))

    toReturn = '\n'
    toReturn += "skuteczność to  " + str(recognizednumber) + '/' + str(allTestVideo) + '=' + str(
        recognizednumber / allTestVideo) + '\n'
    toReturn += "skuteczność A to " + str(recognizednumberA) + '/' + str(allA) + '=' + str(
        recognizednumberA / allA) + '\n'
    toReturn += "skuteczność B to " + str(recognizednumberB) + '/' + str(allB) + '=' + str(
        recognizednumberB / allB) + '\n'
    toReturn += "skuteczność C to " + str(recognizednumberC) + '/' + str(allC) + '=' + str(
        recognizednumberC / allC) + '\n'

    # for class A
    # print("statystyka A 1")
    # for key, value in statisticListA.items():
    #     print(str(key) + " " + str(value[0]))
    # print("statystyka A 2")
    # for key, value in statisticListA.items():
    #     print(str(key) + " " + str(value[1]))
    #
    # print("statystyka B 1")
    # for key, value in statisticListB.items():
    #     print(str(key) + " " + str(1-value[0]))
    # print("statystyka B 2")
    # for key, value in statisticListB.items():
    #     print(str(key) + " " + str(value[1]))

    print(" countA " + str(countA) + " countB " + str(countB) + " countC " + str(countC) + " countD " + str(
        countD) + " countE " + str(countE) + " countF " + str(countF))
    print (deciziontree)
    print (classesForLearning)
    print (len(deciziontree), len(classesForLearning))

    clf = tree.DecisionTreeClassifier(max_depth=7)
    clf = clf.fit(deciziontree[0:40], classesForLearning[0:40])
    prediction= (clf.predict(deciziontree))
    dot_data = tree.export_graphviz(clf, out_file=None,
                                    feature_names=['Atrybut 1','Atrybut 2','Atrybut 3','Atrybut 4','Atrybut 5','Atrybut 6'],
                                    class_names=['Klasa A','Klasa B','Klasa C'],
                                    filled=True, rounded=True,
                                    special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render("iris")

    graph

    i=0
    for key, value in predictedMap.items():

        print("video" + key + "  " + properMap[key] + " " + prediction[i])
        if properMap[key]==prediction[i]:
            i=i+1
    print(i/102)
    return [recognizednumber / allTestVideo, toReturn]


class_list = ['class_1', 'class_2', 'class_3']

string = classify_videos()
print(string)

