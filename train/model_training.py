from filmsanalysis.video_analyse import *
from hmmlearn import hmm
from sklearn.externals import joblib
import random
import matplotlib.pyplot as plt


def get_training_sequences(class_name, trainingLists=[[9,20,14,19,10,42,44,47,48,49],[33,27,15,6,72,73,74,76,77],[38,40,82,83,84]]):
    all_sequences_for_video = []

    if class_name=='class_1':
        for i in trainingLists[0]:
          all_sequences_for_video.append('test_data/sequences_video_' + str(i) + '.txt')
    if class_name=='class_2':
        for i in trainingLists[1]:
          all_sequences_for_video.append('test_data/sequences_video_' + str(i) + '.txt')
    if class_name=='class_3':
        for i in trainingLists[2]:
          all_sequences_for_video.append('test_data/sequences_video_' + str(i) + '.txt')

    all_sequences=[]

    for s in all_sequences_for_video:
        observation = joblib.load(s)
        if len(observation) > 23:
            observation = observation[0:23]
        if len(observation) > 0:
            all_sequences.append(observation)

    return all_sequences

# def get_training_sequences(class_name):
#     all_sequences_for_video = []
#
#     path = 'videos/' + class_name
#     print(path)
#     video_paths = [os.path.join(path, f) for f in os.listdir(path)]
#     print(video_paths)
#     video_paths = get_immediate_subdirectories(path)
#     print(video_paths)
#     for video_path in video_paths:
#         if 'video_' in video_path:
#             print(video_path)
#             all_sequences_for_video.append(video_analyse(path + '/' + video_path))
#
#     return all_sequences_for_video


def train_model(class_name,trainingLists=[[20, 46, 1, 9, 44, 59, 47, 52, 17], [22, 34, 75, 102, 91, 74, 26], [84, 83, 85]]):
    all_sequences_for_video=get_training_sequences(class_name,trainingLists)
    # print(all_sequences_for_video)
    X = np.concatenate(all_sequences_for_video)
    lengths = []
    random_number=str(random.seed())
    joblib.dump(all_sequences_for_video, "models/sequences_" + class_name+".txt")
    state_number = find_state_quantity(all_sequences_for_video, 20,class_name)
    for seq in all_sequences_for_video:
        lengths.append(len(seq))

    remodel = hmm.GaussianHMM(n_components=state_number, n_iter=100)
    remodel.fit(X, lengths)


    return remodel


def find_state_quantity(all_sequences_for_video,max_state=100,file_name='figure'):
    X = np.concatenate(all_sequences_for_video)
    # print(X)
    likelihoods={}
    lengths = []
    state_number = 0

    for seq in all_sequences_for_video:
        lengths.append(len(seq))
    x_list=[]
    y_list=[]
    for x in range(2, max_state):
        remodel = hmm.GaussianHMM(n_components=x, n_iter=100)
        remodel.fit(X, lengths)
        likelihoods[x]=(remodel.score(X, lengths))
        x_list.append(x)
        y_list.append(likelihoods[x])

    plt.plot(x_list,y_list)
    plt.savefig('models/'+file_name)
    state_number=max(likelihoods, key=likelihoods.get)
    print(state_number)
    return state_number




