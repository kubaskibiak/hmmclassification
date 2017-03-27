import cv2, os
import numpy as np
from PIL import Image
from collections import Counter


def getImagesAndLabels(path, face_cascade):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        if 'Thumbs' not in imagePath:
            # print (imagePath)
            # loading the image and converting it to gray scale
            pilImage = Image.open(imagePath).convert('L')
            # Now we are converting the PIL image into numpy array
            imageNp = np.array(pilImage, 'uint8')
            # getting the Id from the image
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces = face_cascade.detectMultiScale(imageNp)
            # If a face is there then append that in the list as well as Id of it
            for (x, y, w, h) in faces:
                img = cv2.resize(imageNp[y:y + h, x:x + w], (200, 200))
                faceSamples.append(img)
                Ids.append(Id)
    return faceSamples, Ids


def trainRecognizer(path, face_cascade, recognizer):
    faces, Ids = getImagesAndLabels(path, face_cascade)
    recognizer.train(faces, np.array(Ids))
    recognizer.save('trainner/trainner.yml')


def computeImageId(path, label):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    maxImageId = 0
    for imagePath in imagePaths:
        if 'Thumbs' not in imagePath and ('User.' + str(label)) in imagePath:
            Id = int(os.path.split(imagePath)[-1].split(".")[2])
            if Id > maxImageId:
                maxImageId = Id
    return maxImageId + 1


def computePersonId(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    maxPersonId = 0;
    for imagePath in imagePaths:
        if 'Thumbs' not in imagePath and 'User.' in imagePath:
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            if Id > maxPersonId:
                maxPersonId = Id
    return maxPersonId + 1


def getVideosList(path):
    videoPaths = [os.path.join(path, f) for f in os.listdir(path)]
    video_list = []
    for videoPath in videoPaths:
        if 'Thumbs' not in videoPath and ('.mkv') in videoPath:
            video_list.append(videoPath)
    video_list.sort()
    return video_list





def add_new_faces(faces, database_path):
    person_id = computePersonId(database_path)
    for person in range(len(faces)):
        for image in range(len(faces[person])):
            if computeImageId(database_path, person_id) < 20:
                cv2.imwrite(database_path + "/User." + str(person_id) + '.' + str(
                    computeImageId(database_path, person_id)) + ".jpg", faces[person][image])

        person_id = person_id + 1


def most_common(lst):
    data = Counter(lst)
    print(data)
    if len(data)>1:
        print(data.most_common(2))
        if(data.most_common(2)[0][0]==(0,False,True,False)):
           return data.most_common(2)[1][0]

    return data.most_common(1)[0][0]


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def is_close_shot(image_height, face_height, treshold):
    if face_height/image_height > treshold:
        return True
    return False