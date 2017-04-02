
from utils.utils import *
import math
class Detector:
    #wykorzystywane klasyfikatory
    profile_face_cascade=cv2.CascadeClassifier('resources/haarcascade_profileface.xml')
    frontal_face_cascade = cv2.CascadeClassifier('resources/haarcascade_frontalface_alt.xml')
    eye_cascade = cv2.CascadeClassifier('resources/haarcascade_eye_tree_eyeglasses.xml')
    mouth_cascade = cv2.CascadeClassifier('resources/haarcascade_mcs_mouth.xml')
    nose_cascade = cv2.CascadeClassifier('resources/haarcascade_mcs_nose.xml')


    # sprawdza czy jest to twarz ludzka - na podstawie skóry i elementów na twarzy
    def check_if_human(self, face_img):
        skindetect=SkinDetector();

        side = math.sqrt(face_img.size)
        minlen = int(side / 10)
        maxlen = int(side / 2)
        eyes = self.eye_cascade.detectMultiScale(face_img, 1.05, 3,minSize=(minlen,minlen),maxSize=(maxlen,maxlen))
        mouth = self.mouth_cascade.detectMultiScale(face_img, 1.05, 3,minSize=(minlen,minlen),maxSize=(maxlen,maxlen))
        nose = self.nose_cascade.detectMultiScale(face_img, 1.05, 3,minSize=(minlen,minlen),maxSize=(maxlen,maxlen))
        check_skin=skindetect.check_skin(face_img ,0.1)
        check_face=len(eyes) ==2 or  (len(mouth) == 1 and len(nose) == 1)
        #print("dobra skóra " + str(check_skin) )
        #print("ma częsci składowe" + str(check_face))
        return  check_skin or check_face

    #detejcha twarzy - zwraca listę wykrytych twarzy
    def detect(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        side = math.sqrt(img.size)
        minlen = int(side / 20)
        maxlen = int(side / 2)
        faces = self.frontal_face_cascade.detectMultiScale(gray, scaleFactor=1.5,minNeighbors=6, minSize=(minlen,minlen),maxSize=(maxlen,maxlen),flags=cv2.CASCADE_SCALE_IMAGE)

        faces_to_return=[]
        if len(faces)>0:
            for (x, y, w, h) in faces:
                face_img = img[int(y):int(y + h), int(x):int(x + w)]
                cv2.imshow('img2', face_img)
                if  self.check_if_human(face_img):
                    faces_to_return.append((x, y, w, h))
        #print(len(faces_to_return))
        return faces_to_return
'''
        if len(faces_to_return)==0:
            print("probuje")
            faces=self.profile_face_cascade.detectMultiScale(gray, scaleFactor=1.2,minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
'''


#detekcja odcienia skóry
class SkinDetector():


    def _R1(self, BGR):
        # channels
        B = BGR[:, :, 0]
        G = BGR[:, :, 1]
        R = BGR[:, :, 2]
        e1 = (R > 95) & (G > 40) & (B > 20) & (
        (np.maximum(R, np.maximum(G, B)) - np.minimum(R, np.minimum(G, B))) > 15) & (np.abs(R - G) > 15) & (R > G) & (
             R > B)
        e2 = (R > 220) & (G > 210) & (B > 170) & (abs(R - G) <= 15) & (R > B) & (G > B)
        return (e1 | e2)

    def _R2(self, YCrCb):
        Y = YCrCb[:, :, 0]
        Cr = YCrCb[:, :, 1]
        Cb = YCrCb[:, :, 2]
        e1 = Cr <= (1.5862 * Cb + 20)
        e2 = Cr >= (0.3448 * Cb + 76.2069)
        e3 = Cr >= (-4.5652 * Cb + 234.5652)
        e4 = Cr <= (-1.15 * Cb + 301.75)
        e5 = Cr <= (-2.2857 * Cb + 432.85)
        return e1 & e2 & e3 & e4 & e5

    def _R3(self, HSV):
        H = HSV[:, :, 0]
        S = HSV[:, :, 1]
        V = HSV[:, :, 2]
        return ((H < 25) | (H > 230))

    def detect(self, src):
        if np.ndim(src) < 3:
            return np.ones(src.shape, dtype=np.uint8)
        if src.dtype != np.uint8:
            return np.ones(src.shape, dtype=np.uint8)
        srcYCrCb = cv2.cvtColor(src, cv2.COLOR_BGR2YCR_CB)
        srcHSV = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
        skinPixels = self._R1(src) & self._R2(srcYCrCb) & self._R3(srcHSV)
        return np.asarray(skinPixels, dtype=np.uint8)

    def check_skin(self,face,treshold):
        skinPixels = self.detect(face)
        skinPercentage = float(np.sum(skinPixels)) / skinPixels.size

        if skinPercentage > treshold:
            return True
        return False
