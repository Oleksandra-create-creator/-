import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox,
    QCheckBox, QSlider, QSpinBox, QProgressBar
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛБ №4 — Завдання 1: Базові віджети")
        self.setMinimumSize(600, 450)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        title_label = QLabel("Демонстрація базових віджетів PyQt6")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setToolTip("Це заголовок вікна")
        main_layout.addWidget(title_label)

        form_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Введіть ім'я:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Наприклад, Марія")
        self.name_input.setToolTip("Поле для введення імені")
        left_layout.addWidget(self.name_input)

        left_layout.addWidget(QLabel("Оберіть мову:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Python", "JavaScript", "Java", "C++", "Go"])
        self.lang_combo.setToolTip("Випадаючий список мов програмування")
        left_layout.addWidget(self.lang_combo)

        self.agree_check = QCheckBox("Я згодна з умовами")
        self.agree_check.setChecked(True)
        self.agree_check.setToolTip("Прапорець згоди")
        left_layout.addWidget(self.agree_check)

        form_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Гучність:"))
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.setToolTip("Повзунок гучності")
        right_layout.addWidget(self.slider)

        right_layout.addWidget(QLabel("Кількість спроб:"))
        self.spin_box = QSpinBox()
        self.spin_box.setRange(1, 100)
        self.spin_box.setValue(10)
        self.spin_box.setToolTip("Лічильник спроб")
        right_layout.addWidget(self.spin_box)

        right_layout.addWidget(QLabel("Прогрес завантаження:"))
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(30)
        self.progress_bar.setToolTip("Індикатор прогресу")
        right_layout.addWidget(self.progress_bar)

        form_layout.addLayout(right_layout)
        main_layout.addLayout(form_layout)

        main_layout.addWidget(QLabel("Коментарі:"))
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Введіть свої нотатки тут...")
        self.text_edit.setToolTip("Багаторядкове текстове поле")
        main_layout.addWidget(self.text_edit)

        self.submit_btn = QPushButton("Надіслати")
        self.submit_btn.setEnabled(True)
        self.submit_btn.setToolTip("Натисніть для надсилання даних")
        main_layout.addWidget(self.submit_btn)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
