from  filmsanalysis.video_analyse import *
from train.model_training import *
import shutil

video_analyse("videos/class_996/video_103")
# observation=joblib.load('models/sequences_class_2.txt')
# print (observation)

#tworzenie folderów ze zdjęciem


for i in range(0,106):
    os.mkdir("C:/Users/kuba/Desktop/project/hmmclassification/dataSet/class_998/video_" + str(i))
    shutil.copy2('C:/Users/kuba/Desktop/project/hmmclassification/dataSet/User.1.0.jpg', "C:/Users/kuba/Desktop/project/hmmclassification/dataSet/class_998/video_" + str(i))