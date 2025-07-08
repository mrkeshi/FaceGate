import os
from PySide6.QtWidgets import QInputDialog, QMessageBox, QListWidget, QListWidgetItem
import recognizer
import storage

def get_name_input(parent):
    name, ok = QInputDialog.getText(parent, "ورود نام", "نام فرد را وارد کنید:")
    return name, ok

def add_face(name):
    return recognizer.replace_face(name)

def get_all_faces():
    return storage.get_all_faces()

def delete_face(face_id):
    return storage.delete_face_by_id(face_id)

def start_camera_action():
    recognizer.start_camera()

def show_logs_action(main_window):
    main_window.show_logs_page()

def exit_action():
    import sys
    sys.exit()

def get_logs():
    return storage.get_logs()
