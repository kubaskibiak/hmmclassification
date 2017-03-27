from video_analyse import *
from hmmlearn import hmm
from sklearn.externals import joblib


def get_training_sequences(class_name):
    all_sequences_for_video = []

    path = 'videos/' + class_name
    print(path)
    video_paths = [os.path.join(path, f) for f in os.listdir(path)]
    print(video_paths)
    video_paths = get_immediate_subdirectories(path)
    print(video_paths)
    for video_path in video_paths:
        if 'video_' in video_path:
            print(video_path)
            all_sequences_for_video.append(video_analyse(path + '/' + video_path))

    return all_sequences_for_video


def train_model(all_sequences_for_video):
    X = np.concatenate(all_sequences_for_video)
    lengths = []
    joblib.dump(all_sequences_for_video, "Output2.txt")
    state_number = find_state_quantity(all_sequences_for_video, 20)
    for seq in all_sequences_for_video:
        lengths.append(len(seq))

    remodel = hmm.GaussianHMM(n_components=state_number, n_iter=100)
    remodel.fit(X, lengths)


    text_file = open("Output.txt", "w")
    text_file.write(str(all_sequences_for_video))
    text_file.close()

    return remodel


def find_state_quantity(all_sequences_for_video,max_state=100):
    X = np.concatenate(all_sequences_for_video)
    print(X)
    likelihoods={}
    lengths = []
    state_number = 0

    for seq in all_sequences_for_video:
        lengths.append(len(seq))

    for x in range(1, max_state):
        remodel = hmm.GaussianHMM(n_components=x, n_iter=100)
        remodel.fit(X, lengths)
        likelihoods[x]=(remodel.score(X, lengths))

    state_number=max(likelihoods, key=likelihoods.get)
    print(state_number)
    return state_number

class_list = ['class_1']
print(class_list)
for single_class in class_list:
    print(class_list)
    sequences = get_training_sequences(single_class)
    model = train_model(sequences)

    joblib.dump(model, "models/model_for_" + single_class + ".pkl")


