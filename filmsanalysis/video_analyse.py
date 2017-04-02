from utils.utils import *
from filmsanalysis.shot_analyse import *
from classes.observation import *

# analyze result


def video_analyse(video_path):
    print(video_path)
    shot_list = getVideosList(video_path)
    observation_sequence = []

    data_base_path = "dataSet/" + video_path[video_path.find("/") + 1:]

    print(data_base_path + "")
    shot_counter =0

    list_of_person_sets=[]
    previously_recognized=set()
    for video_path in shot_list:
        # new shot state
        was_n_shot_erlier=0

        #observation_sequence.append(Observation(is_first_frame=True).symbol)
        observation_sequence.append((0, False, False, 0, True))
        #print((0, False, False, True))
        sequence,recognized_people=get_observable_sequence(video_path, data_base_path, 20)
        common_element = most_common(sequence)
        if(common_element[2]==True):
            was_n_shot_erlier = 100
            if (shot_counter >= 2):
                if len(recognized_people & list_of_person_sets[shot_counter - 2]) > 0:
                    was_n_shot_erlier = 2
            if(shot_counter>=1):
                if len(recognized_people & list_of_person_sets[shot_counter - 1]) > 0:
                    was_n_shot_erlier = 1




        print(was_n_shot_erlier)
        print ("OPIS UJĘCIA:")
        print(common_element)
        print (Observation(common_element[0],common_element[1],common_element[2],was_n_shot_erlier,common_element[3]))
        observation_sequence.append((common_element[0],common_element[1],common_element[2],was_n_shot_erlier,common_element[3]))
        list_of_person_sets.append(recognized_people)
        shot_counter+=1

    cv2.destroyAllWindows()
    return observation_sequence

