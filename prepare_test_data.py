from train.model_training import *

video_list=[]
for i in range(17,106):
    if i not in [7,43,88,29]:
        video_list.append('videos/class_998/video_' + str(i))


for video in video_list:
    observations=video_analyse(video)
    joblib.dump(observations, "test_data/sequences_" + video.split('/')[2]+".txt")



