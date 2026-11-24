import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QCheckBox
)
from PyQt6.QtCore import pyqtSignal, Qt


class FilterPanel(QWidget):
    filter_changed = pyqtSignal(str)
    clear_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Фільтр:"))
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Введіть текст для фільтрації")
        layout.addWidget(self.filter_input)

        self.block_check = QCheckBox("Блокувати сигнали")
        layout.addWidget(self.block_check)

        self.filter_input.textChanged.connect(self._on_text_changed)
        self.block_check.toggled.connect(self._on_block_toggled)

    def _on_text_changed(self, text: str):
        self.filter_changed.emit(text)

    def _on_block_toggled(self, checked: bool):
        if checked:
            self.filter_input.blockSignals(True)
            self.filter_input.clear()
        else:
            self.filter_input.blockSignals(False)

    def reset(self):
        self.filter_input.blockSignals(False)
        self.block_check.setChecked(False)
        self.filter_input.clear()
        self.clear_requested.emit()


class ResultPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Результати:"))
        self.result_list = QListWidget()
        layout.addWidget(self.result_list)

        self.all_items = [
            "Python", "JavaScript", "Java", "C++", "Go",
            "Rust", "TypeScript", "Ruby", "Swift", "Kotlin"
        ]
        self._populate()

    def _populate(self):
        self.result_list.clear()
        for item in self.all_items:
            self.result_list.addItem(item)

    def apply_filter(self, text: str):
        self.result_list.clear()
        for item in self.all_items:
            if text.lower() in item.lower():
                self.result_list.addItem(item)

    def reset(self):
        self._populate()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛБ №4 — Завдання 4: Кастомні сигнали")
        self.setMinimumSize(600, 400)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        self.filter_panel = FilterPanel()
        self.result_panel = ResultPanel()

        main_layout.addWidget(self.filter_panel)
        main_layout.addWidget(self.result_panel)

        self.filter_panel.filter_changed.connect(self.result_panel.apply_filter)
        self.filter_panel.clear_requested.connect(self.result_panel.reset)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
