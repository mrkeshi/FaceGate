# main.py
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QListWidget, QMessageBox, QHBoxLayout, QListWidgetItem
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
import actions
import storage
import os


class ManageFacesPage(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.setWindowTitle("مدیریت چهره‌ها")
        self.setup_ui()
        self.load_faces()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.faces_list = QListWidget()
        self.layout.addWidget(self.faces_list)

        btn_layout = QHBoxLayout()

        self.back_button = QPushButton("بازگشت")
        self.back_button.clicked.connect(self.go_back_callback)
        btn_layout.addWidget(self.back_button)

        self.delete_button = QPushButton("حذف")
        self.delete_button.clicked.connect(self.delete_face)
        btn_layout.addWidget(self.delete_button)

        self.add_button = QPushButton("اضافه کردن")
        self.add_button.clicked.connect(self.add_face)
        btn_layout.addWidget(self.add_button)

        self.layout.addLayout(btn_layout)

    def load_faces(self):
        self.faces_list.clear()
        faces = actions.get_all_faces()
        for face in faces:
            item = QListWidgetItem()
            item.setText(f"{face['name']} - {face['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            if 'image_path' in face and os.path.exists(face['image_path']):
                pixmap = QPixmap(face['image_path']).scaled(64, 64, Qt.KeepAspectRatio)
                icon = QIcon(pixmap)
                item.setIcon(icon)
            self.faces_list.addItem(item)

    def delete_face(self):
        current_row = self.faces_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "هشدار", "لطفا یک چهره را انتخاب کنید")
            return
        face = actions.get_all_faces()[current_row]
        reply = QMessageBox.question(self, "تایید حذف", f"حذف {face['name']}?")
        if reply == QMessageBox.Yes:
            actions.delete_face(face["_id"])
            self.load_faces()

    def add_face(self):
        name, ok = actions.get_name_input(self)
        if ok and name.strip():
            success = actions.add_face(name.strip())  # اصلاح این خط
            if success:
                QMessageBox.information(self, "موفقیت", f"چهره {name} ذخیره شد")
                self.load_faces()
            else:
                QMessageBox.warning(self, "خطا", "کاری نشد")


class LogsPage(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.setup_ui()
        self.load_logs()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.logs_list = QListWidget()
        self.logs_list.setIconSize(QSize(250, 250))  # اینجا اندازه آیکون رو تنظیم میکنیم
        layout.addWidget(self.logs_list)

        back_button = QPushButton("بازگشت")
        back_button.clicked.connect(self.go_back_callback)
        layout.addWidget(back_button)

    def load_logs(self):
        self.logs_list.clear()
        logs = actions.get_logs()
        for log in logs:
            name = log.get("name", "ناشناس")
            status = log.get("status", "-")
            time_str = log["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            text = f"{name} - {status} - {time_str}"
            item = QListWidgetItem(text)

            # اگر تصویر موجود بود، به آیکون آیتم اضافه کن و اندازه تصویر را 250 تنظیم کن
            if "image_path" in log and log["image_path"] and os.path.exists(log["image_path"]):
                pixmap = QPixmap(log["image_path"]).scaled(250, 250, Qt.KeepAspectRatio)
                icon = QIcon(pixmap)
                item.setIcon(icon)

            self.logs_list.addItem(item)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FaceGate")
        self.setFixedSize(700, 550)
        self.show_main_page()

    def show_main_page(self):
        main_widget = QWidget()
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        def style_button(btn):
            btn.setFixedHeight(80)
            btn.setMinimumWidth(350)  # عرض بیشتر دکمه‌ها
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 22px;
                    font-weight: bold;
                    color: white;
                    background-color: #009688;
                    border-radius: 20px;
                    padding: 10px;  /* کاهش padding */
                    margin: 6px;    /* کاهش margin */
                }
                QPushButton:hover {
                    background-color: #00796b;
                }
                QPushButton:pressed {
                    background-color: #004d40;
                }
            """)

        start_button = QPushButton("شروع نظارت")
        manage_button = QPushButton("مدیریت چهره‌ها")
        logs_button = QPushButton("لاگ‌ها")
        exit_button = QPushButton("خروج")

        for btn in [start_button, manage_button, logs_button, exit_button]:
            style_button(btn)
            layout.addWidget(btn)

        start_button.clicked.connect(actions.start_camera_action)
        manage_button.clicked.connect(self.show_manage_faces_page)
        logs_button.clicked.connect(self.show_logs_page)
        exit_button.clicked.connect(self.close)

        self.setCentralWidget(main_widget)

    def show_manage_faces_page(self):
        self.manage_page = ManageFacesPage(self.show_main_page)
        self.setCentralWidget(self.manage_page)

    def show_logs_page(self):
        self.logs_page = LogsPage(self.show_main_page)
        self.setCentralWidget(self.logs_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
