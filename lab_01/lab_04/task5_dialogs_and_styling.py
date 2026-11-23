import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QDialog, QFormLayout,
    QMessageBox, QInputDialog, QColorDialog, QListWidget
)
from PyQt6.QtCore import Qt


GLOBAL_STYLE = """
    QMainWindow {
        background-color: #f5f5f5;
    }
    QLabel {
        font-family: 'Segoe UI', 'Arial', sans-serif;
        font-size: 13px;
        color: #333333;
    }
    QPushButton {
        background-color: #4a90e2;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-size: 13px;
    }
    QPushButton:hover {
        background-color: #357abd;
    }
    QPushButton:pressed {
        background-color: #2a5f9e;
    }
    QPushButton:disabled {
        background-color: #cccccc;
    }
    QLineEdit {
        border: 1px solid #cccccc;
        border-radius: 4px;
        padding: 6px;
        font-size: 13px;
    }
    QLineEdit:focus {
        border: 1px solid #4a90e2;
    }
    QListWidget {
        border: 1px solid #dddddd;
        border-radius: 4px;
        padding: 4px;
        background-color: white;
    }
"""


class UserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Додати користувача")
        self.setMinimumWidth(350)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Наприклад, Олена")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@mail.com")

        form_layout = QFormLayout()
        form_layout.addRow("Ім'я:", self.name_input)
        form_layout.addRow("Email:", self.email_input)

        buttons_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Додати")
        self.cancel_btn = QPushButton("Скасувати")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #999999;
            }
            QPushButton:hover {
                background-color: #777777;
            }
        """)
        buttons_layout.addWidget(self.ok_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "email": self.email_input.text().strip()
        }


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛБ №4 — Завдання 5: Діалоги та стилізація")
        self.setMinimumSize(600, 450)
        self.setStyleSheet(GLOBAL_STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.welcome_label = QLabel("Ласкаво просимо! Оберіть дію.")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.welcome_label)

        self.user_list = QListWidget()
        layout.addWidget(self.user_list)

        buttons_layout = QHBoxLayout()

        self.msg_btn = QPushButton("Повідомлення")
        self.msg_btn.clicked.connect(self.show_message_dialog)
        buttons_layout.addWidget(self.msg_btn)

        self.input_btn = QPushButton("Ввести дані")
        self.input_btn.clicked.connect(self.show_input_dialog)
        buttons_layout.addWidget(self.input_btn)

        self.form_btn = QPushButton("Додати користувача")
        self.form_btn.clicked.connect(self.show_custom_dialog)
        buttons_layout.addWidget(self.form_btn)

        self.color_btn = QPushButton("Змінити колір")
        self.color_btn.clicked.connect(self.change_color)
        buttons_layout.addWidget(self.color_btn)

        layout.addLayout(buttons_layout)

    def show_message_dialog(self):
        result = QMessageBox.question(
            self,
            "Підтвердження",
            "Ви впевнені, що хочете очистити список?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if result == QMessageBox.StandardButton.Yes:
            self.user_list.clear()
            self.welcome_label.setText("Список очищено")

    def show_input_dialog(self):
        text, ok = QInputDialog.getText(
            self, "Введення даних", "Введіть повідомлення для відображення:"
        )
        if ok and text:
            self.welcome_label.setText(text)

    def show_custom_dialog(self):
        dialog = UserDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data["name"] and data["email"]:
                self.user_list.addItem(f"{data['name']} — {data['email']}")
                self.welcome_label.setText(f"Додано: {data['name']}")

    def change_color(self):
        color = QColorDialog.getColor(parent=self, title="Оберіть колір")
        if color.isValid():
            self.welcome_label.setStyleSheet(f"color: {color.name()}; font-size: 16px;")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
