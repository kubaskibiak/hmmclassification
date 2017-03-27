import cv2,os
import numpy as np
from PIL import Image
from hmmlearn import hmm
import time
from utils.utils  import *
from sklearn.externals import joblib



face_cascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('resources/haarcascade_eye_tree_eyeglasses.xml')
mouth_cascade = cv2.CascadeClassifier('resources/haarcascade_mcs_mouth.xml')
nose_cascade = cv2.CascadeClassifier('resources/haarcascade_mcs_nose.xml')
        
def get_observable_sequence(path,database_path,skipped):

        recognizer = cv2.face.createLBPHFaceRecognizer()
        #recognizer = cv2.face.createEigenFaceRecognizer()
        #recognizer = cv2.face.createFisherFaceRecognizer()

        cap = cv2.VideoCapture(path)
        trainRecognizer(database_path,face_cascade,recognizer)

        #skipping frames
        counter=0;
        skip=skipped
        #observated symbols
        observation_sequence=[]
        observation=[]

        #symbol params
        many_faces=False;
        is_new=False


        #used in adding
        faces_to_add=[]
        
        while True :

                #break if video is ended
                ret, img = cap.read()
                if  not ret:
                    break
                #resize frame (make computing faster)
                img=cv2.resize(img, (0,0), fx=0.3, fy=0.3)

                #use every skip-th frame
                if counter%skip==0:

                    #detecs faces
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.5, 6)

                    face_index=0
                
                    for (x,y,w,h) in faces:
                        person_face=None
                        #recognizing
                        
                        Id, conf = recognizer.predict(cv2.resize(gray[y:y+h,x:x+w], (200, 200)) )
                        face_img=gray[int(y):int(y+h),int(x):int(x+w)]

                      
                        if (check_if_human(face_img,eye_cascade,mouth_cascade,nose_cascade)):
                            #ploting rectangles and identities
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            cv2.putText(img,str(Id )+ ' conf ' + str(conf), (x,y+h),font, 1,(255,0,0))
                            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                            roi_gray = gray[y:y+h, x:x+w]
                            roi_color = img[y:y+h, x:x+w]

                            print ('conf: '+str(conf))

                            #add to dat base only if criterions ale fulfilled.      
                            if conf>60:
                                is_new=True  
                                #check if array is empty
                                if (len(faces_to_add)<=face_index):
                                    faces_to_add.append([])
                                #add face
                                faces_to_add[face_index].append(cv2.resize(gray[y:y+h,x:x+w], (200, 200)))
                                
                               
                            else:               
                                if computeImageId('dataSet',Id)<20:
                                    cv2.imwrite(database_path+"/User."+str(Id) +'.'+ str(computeImageId(database_path,Id)) + ".jpg", cv2.resize(gray[y:y+h,x:x+w], (200, 200)))
                                    #trainRecognizer('dataSet',face_cascade,recognizer)

                        else:
                            continue
                        
                        face_index=face_index+1

                        

                    if len(faces)>1:
                        many_faces=True;

                
                    #print obsevations
                    observation=(len(faces),is_new,many_faces,False)
                    observation_sequence.append(observation)
                    print(observation)
                    
                    cv2.imshow('img',img)
                    
                    is_new=False
                    many_faces=False;            
                    

                
                counter=counter+1
                k = cv2.waitKey(1) & 0xff
                if k == 27:
                     break
        cap.release()
        cv2.destroyAllWindows()
        add_new_faces(faces_to_add,database_path)
        
        return observation_sequence

# analyze result
video_list = getVideosList('videos/class_1/video_1')
observation_sequence=[]
class_nr=1
video_nr=1
for video_path in video_list:
    observation_sequence.append(tuple([0,False,False,True]))
    common_element=most_common(get_observable_sequence(video_path,"dataSet/class_"+str(class_nr)+"/video_"+str(video_nr),2))
    observation_sequence.append(common_element)
        
        
print(observation_sequence)

s = set(observation_sequence)
print (len(s))
print (s)
remodel = hmm.GaussianHMM(n_components=len(s), n_iter=100)
remodel.fit(observation_sequence)


joblib.dump(remodel, "models/class1.pkl")

print(remodel.score(observation_sequence))



           

