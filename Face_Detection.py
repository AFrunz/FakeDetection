import cv2


def face_count(img_path):
    facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.5, 3)
    cv2.destroyAllWindows()
    return len(faces)

