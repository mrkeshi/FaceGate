import cv2
import os
import datetime
from pymongo import MongoClient
from bson import ObjectId
from playsound import playsound
import time
from email_utils import send_failure_email
# پوشه تصاویر
from storage import add_log

IMAGES_DIR = "saved_faces"
os.makedirs(IMAGES_DIR, exist_ok=True)

# صداها
TICK_SOUND = "tick.mp3"
FAIL_SOUND = "fail.mp3"

client = MongoClient("mongodb://localhost:27017/")
db = client["facegate_db"]
faces_collection = db["faces"]
logs_collection = db["logs"]

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def replace_face(name):
    old_faces = list(faces_collection.find({"name": name}))
    for face in old_faces:
        try:
            if os.path.exists(face['image_path']):
                os.remove(face['image_path'])
        except Exception as e:
            print("خطا در حذف فایل قدیمی:", e)
        faces_collection.delete_one({"_id": face["_id"]})

    img_path = capture_face(name)
    if not img_path:
        return False

    face_doc = {
        "name": name,
        "image_path": img_path,
        "timestamp": datetime.datetime.now()
    }
    faces_collection.insert_one(face_doc)
    return True

def capture_face(name):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False

    recognized = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            recognized = True
            face_img = frame[y:y+h, x:x+w]
            img_path = os.path.join(IMAGES_DIR, f"{name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
            cv2.imwrite(img_path, face_img)
            cap.release()
            cv2.destroyAllWindows()
            return img_path

        cv2.imshow("Face Capture", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False

def match_face(frame):

    known_faces = list(faces_collection.find())
    for face in known_faces:
        img = cv2.imread(face['image_path'])
        if img is not None:
            return face['name'], face['image_path']
    return None, None




FAILED_IMAGES_DIR = "failed_entries"
os.makedirs(FAILED_IMAGES_DIR, exist_ok=True)

def save_failed_image(frame):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"failed_{timestamp}.jpg"
    path = os.path.join(FAILED_IMAGES_DIR, filename)
    cv2.imwrite(path, frame)
    return path

def start_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("دوربین باز نشد")
        return

    time.sleep(2)

    ret, frame = cap.read()
    if not ret:
        print("فریم دریافت نشد")
        cap.release()
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        name, img_path = match_face(frame)
        if name:
            status = "موفق"
            color = (0, 255, 0)
            text = name
            try:
                playsound(TICK_SOUND)
            except:
                print("خطا در پخش صدای موفق")
        else:
            status = "ناموفق"
            color = (0, 0, 255)
            text = "unknown"
            img_path = save_failed_image(frame)
            send_failure_email(img_path)

            try:
                playsound(FAIL_SOUND)
            except:
                print("خطا در پخش صدای ناموفق")

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        add_log(text.split(" - ")[0], status, img_path)
    else:
        print("هیچ چهره‌ای شناسایی نشد")

    cap.release()


    cv2.imshow("نتیجه تشخیص چهره", frame)
    cv2.waitKey(3000)
    cap.release()
    cv2.destroyAllWindows()