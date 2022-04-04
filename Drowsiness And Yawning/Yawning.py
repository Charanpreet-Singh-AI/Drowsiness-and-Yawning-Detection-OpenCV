import cv2
import dlib
from scipy.spatial import distance

def calculate_MAR(mouth):
    A = distance.euclidean(mouth[3], mouth[5])
    B = distance.euclidean(mouth[2], mouth[6])
    C = distance.euclidean(mouth[1], mouth[7])
    D = distance.euclidean(mouth[0], mouth[4])
    mar_aspect_ratio = (A+B+C)/(D)
    return mar_aspect_ratio

i=0
cap = cv2.VideoCapture(0)
hog_face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = hog_face_detector(gray)

    for face in faces:
        face_landmarks = dlib_facelandmark(gray, face)
        lip = []
        for n in range(48,60):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            lip.append((x,y))
            next_point = n+1
            if n == 59:
                next_point = 48
            x2 = face_landmarks.part(next_point).x
            y2 = face_landmarks.part(next_point).y
            cv2.line(frame,(x,y),(x2,y2),(0,255,0),1)

        lip_mar = calculate_MAR(lip)
        MAR = round(lip_mar, 2)

        if MAR >= 2.5:
            i += 1

            print("Yawning")

            cv2.putText(frame,Yawning, (10, 400),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        #cv2.putText(frame,"No. of counts =", (10, 400),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        #cv2.putText(frame,str(i), (20, 450),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        print(MAR,i)

    cv2.imshow("Are you Sleepy", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()

