import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QCheckBox, QMessageBox
)
from PyQt6.QtCore import Qt


def external_slot_handler(value: str):
    print(f"[Зовнішня функція-слот] Отримано значення: {value}")


class FormWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛБ №4 — Завдання 2: Інтерактивна форма")
        self.setMinimumSize(500, 400)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        layout.addWidget(QLabel("Ім'я:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введіть ваше ім'я")
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Вік:"))
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Від 1 до 120")
        layout.addWidget(self.age_input)

        layout.addWidget(QLabel("Місто:"))
        self.city_combo = QComboBox()
        self.city_combo.addItems(["Київ", "Львів", "Одеса", "Харків", "Дніпро"])
        layout.addWidget(self.city_combo)

        self.subscribe_check = QCheckBox("Підписатися на розсилку")
        layout.addWidget(self.subscribe_check)

        self.result_label = QLabel("Тут з'явиться результат")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        buttons_layout = QHBoxLayout()
        self.submit_btn = QPushButton("Підтвердити")
        self.reset_btn = QPushButton("Скинути")
        buttons_layout.addWidget(self.submit_btn)
        buttons_layout.addWidget(self.reset_btn)
        layout.addLayout(buttons_layout)

        self.name_input.textChanged.connect(self.update_result_label)
        self.name_input.textChanged.connect(external_slot_handler)
        self.city_combo.currentTextChanged.connect(
            lambda text: self.result_label.setText(f"Обрано місто: {text}")
        )
        self.subscribe_check.toggled.connect(self.submit_btn.setEnabled)
        self.submit_btn.clicked.connect(self.validate_and_submit)
        self.reset_btn.clicked.connect(self.reset_form)

        self.submit_btn.setEnabled(False)
        self.reset_form()

    def update_result_label(self, text: str):
        if text:
            self.result_label.setText(f"Привіт, {text}!")
        else:
            self.result_label.setText("Тут з'явиться результат")

    def validate_and_submit(self):
        name = self.name_input.text().strip()
        age_text = self.age_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Помилка", "Ім'я не може бути порожнім!")
            return

        if not age_text.isdigit():
            QMessageBox.warning(self, "Помилка", "Вік має бути числом!")
            return

        age = int(age_text)
        if age < 1 or age > 120:
            QMessageBox.warning(self, "Помилка", "Вік має бути від 1 до 120!")
            return

        city = self.city_combo.currentText()
        subscribed = "так" if self.subscribe_check.isChecked() else "ні"
        QMessageBox.information(
            self,
            "Успіх",
            f"Дані збережено!\nІм'я: {name}\nВік: {age}\nМісто: {city}\nПідписка: {subscribed}"
        )

    def reset_form(self):
        self.name_input.clear()
        self.age_input.clear()
        self.city_combo.setCurrentIndex(0)
        self.subscribe_check.setChecked(False)
        self.result_label.setText("Тут з'явиться результат")
        self.submit_btn.setEnabled(False)


def main():
    app = QApplication(sys.argv)
    window = FormWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
