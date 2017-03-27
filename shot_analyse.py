from frame_analyse import *
from facedet.detector import *

face_cascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('resources/haarcascade_eye_tree_eyeglasses.xml')
mouth_cascade = cv2.CascadeClassifier('resources/haarcascade_mcs_mouth.xml')
nose_cascade = cv2.CascadeClassifier('resources/haarcascade_mcs_nose.xml')

detector = Detector()


def get_observable_sequence(path, database_path, skipped):
    recognizer = cv2.face.createLBPHFaceRecognizer()
    # recognizer = cv2.face.createEigenFaceRecognizer()
    # recognizer = cv2.face.createFisherFaceRecognizer()

    cap = cv2.VideoCapture(path)
    trainRecognizer(database_path, face_cascade, recognizer)

    # skipping frames
    counter = 0;
    skip = skipped
    # observed symbols
    observation_sequence = []
    person_in_image=set()

    # symbol params


    # used in adding
    faces_to_add = []

    while True:
        faces_from_frame = []
        # break if video is ended
        ret, img = cap.read()
        if not ret:
            break

        # use every skip-th frame
        if counter % skip == 0:
            observation, faces_from_frame ,recognized_persons = label_image(img, database_path, recognizer,detector)
            observation_sequence.append(observation)

            while len(faces_from_frame) > len(faces_to_add):
                faces_to_add.append([])

            face_index = 0

            for face in faces_from_frame:
                faces_to_add[face_index].append(face)

                face_index += 1
            person_in_image.update(recognized_persons)
        counter += 1
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    cap.release()

    if len(faces_to_add) > 0:
        if len(faces_to_add[0])/(counter/skip) >0.1:
            add_new_faces(faces_to_add, database_path)

    return observation_sequence,person_in_image
