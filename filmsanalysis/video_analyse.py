from filmsanalysis.shot_analyse import *
from observation.observation import *

# analyze result


def video_analyse(video_path):

    print(video_path)
    shot_list = getVideosList(video_path) #list of shots
    observation_sequence = []
    data_base_path = "dataSet/" + video_path[video_path.find("/") + 1:]
    shot_counter =0
    list_of_person_sets=[]

    print(video_path)
    print(data_base_path + "")


    # save recognized persons per shot
    file = open(data_base_path+'_recognizedPersons.txt', 'w')
    shot_number=1

    #analysis of all shots
    for video_path in shot_list:
        # new shot state
        was_n_shot_erlier=0
        observation_sequence.append((0, False, False, 0, True))

        ########analysis of signle shot
        sequence,recognized_people=get_observable_sequence(video_path, data_base_path, 40)
        common_element = most_common(sequence)

        if(common_element[2]==True):
            was_n_shot_erlier = 100
            if (shot_counter >= 2):
                if len(recognized_people & list_of_person_sets[shot_counter - 2]) > 0:
                    was_n_shot_erlier = 2
            if(shot_counter>=1):
                if len(recognized_people & list_of_person_sets[shot_counter - 1]) > 0:
                    was_n_shot_erlier = 1

        print("SHOT " +str(shot_number) + " recognized: "+str(recognized_people) +'\n')
        file.write("SHOT " +str(shot_number) + " recognized: "+str(recognized_people) +'\n' )
        shot_number=shot_number+1


        #print(was_n_shot_erlier)
        print ("OPIS UJĘCIA:")
        #print(common_element)
        print (Observation(common_element[0],common_element[1],common_element[2],was_n_shot_erlier,common_element[3]))
        observation_sequence.append((common_element[0],common_element[1],common_element[2],was_n_shot_erlier,common_element[3]))
        list_of_person_sets.append(recognized_people)
        shot_counter+=1

        #zabezpiezcenie dla długich filmów, zeby nie trwało to wieki (analiza tylko 60 ujec)
        if shot_counter > 60 :
            break

    cv2.destroyAllWindows()
    return observation_sequence

