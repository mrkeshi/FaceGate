import os
import datetime
from pymongo import MongoClient
from bson import ObjectId

# مسیر پوشه ذخیره عکس‌ها
IMAGES_DIR = "saved_faces"
os.makedirs(IMAGES_DIR, exist_ok=True)

# اتصال به دیتابیس MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["facegate_db"]
faces_collection = db["faces"]
logs_collection = db["logs"]

def get_all_faces():
    return list(faces_collection.find())

def delete_face_by_id(face_id):
    try:
        face = faces_collection.find_one({"_id": ObjectId(face_id)})
        if not face:
            return False
        if os.path.exists(face['image_path']):
            os.remove(face['image_path'])
        faces_collection.delete_one({"_id": ObjectId(face_id)})
        return True
    except Exception as e:
        print("خطا در حذف چهره:", e)
        return False


def get_logs():
    return list(logs_collection.find().sort("timestamp", -1))

def add_log(name, status, image_path=None):

    log_doc = {
        "name": name,
        "status": status,
        "image_path": image_path,
        "timestamp": datetime.datetime.now()
    }
    logs_collection.insert_one(log_doc)

def find_face_by_name(name):
    return faces_collection.find_one({"name": name})
