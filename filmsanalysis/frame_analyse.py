from utils.utils import *


def label_image(img, database_path, recognizer, detector):
    # resize frame (make computing faster)
    img = cv2.resize(img, (0, 0), fx=1, fy=1)
    person_in_image=set()
    # detect faces
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detect(img)
    many_faces = False
    is_in_DB = True
    is_close_shot = False
    faces_to_add = []

    for (x, y, w, h) in faces:

        face_img = gray[int(y):int(y + h), int(x):int(x + w)]


        # recognizing
        Id, conf = recognizer.predict(cv2.resize(gray[y:y + h, x:x + w], (200, 200)))
        person_in_image.add(Id)
        # plotting rectangles and identities
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(Id) + ' conf ' + str(conf), (x, y + h), font, 1, (255, 0, 0))
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        #print('conf: ' + str(conf))

        # add to database only if criterion is fulfilled.
        if conf > 90:
            is_in_DB = False
             # check if array is empty
            faces_to_add.append(cv2.resize(gray[y:y + h, x:x + w], (200, 200)))
            #cv2.imshow('img', cv2.resize(gray[y:y + h, x:x + w], (200, 200)))


        elif conf < 50:
            if computeImageId(database_path, Id) < 20:
                cv2.imwrite(database_path + "/User." + str(Id) + '.' + str(
                    computeImageId(database_path, Id)) + ".jpg",
                                cv2.resize(gray[y:y + h, x:x + w], (200, 200)))
                # trainRecognizer('dataSet',face_cascade,recognizer)
        #sprawdza czy jest zbliżenie na twarz
        if ( h/img.shape[0] > 0.3):
            is_close_shot = True

    if len(faces) > 1:
        many_faces = True;
    else:
        many_faces = False;

    # print observations
    observation = (len(faces),is_close_shot, is_in_DB, False)

    #observation=Observation(num_faces=len(faces),is_close=False, is_in_db=is_new, is_first_frame=False)
    #print(observation)
    cv2.imshow('img', img)


    return observation, faces_to_add, person_in_image
