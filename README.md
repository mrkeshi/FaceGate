# FaceGate - Smart Facial Access Control System

**FaceGate** is an intelligent facial recognition system designed to control access using a webcam. It verifies faces in real time, grants or denies access, logs each event, and can notify an admin.

---

## 🔧 Features

- Live face detection via webcam
- Face registration with name
- Access control: authorized vs. unauthorized
- MongoDB logging (name, time, status)
- Admin notifications (email or panel)
- Clean GUI built with PySide6

---

## 📦 Tech Stack

- Python 3
- OpenCV
- face_recognition
- PySide6 (or PyQt5)
- MongoDB

---

## 🚀 Getting Started

```bash
pip install -r requirements.txt
python main.py
