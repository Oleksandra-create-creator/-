import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ЛБ №4 — Завдання 3: QMainWindow")
        self.setMinimumSize(700, 500)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Почніть друкувати тут...")
        self.setCentralWidget(self.text_edit)

        self._create_menu()
        self._create_toolbar()
        self._create_statusbar()
        self._connect_signals()

    def _create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("Файл")

        new_action = QAction("Новий", self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self.action_new)
        file_menu.addAction(new_action)

        open_action = QAction("Відкрити файл...", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.action_open)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        exit_action = QAction("Вихід", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menu_bar.addMenu("Довідка")

        about_action = QAction("Про програму", self)
        about_action.setShortcut(QKeySequence("F1"))
        about_action.triggered.connect(self.action_about)
        help_menu.addAction(about_action)

        stats_action = QAction("Статистика тексту", self)
        stats_action.triggered.connect(self.action_stats)
        help_menu.addAction(stats_action)

    def _create_toolbar(self):
        toolbar = self.addToolBar("Головна")
        toolbar.setMovable(False)

        new_btn = QAction("Новий", self)
        new_btn.triggered.connect(self.action_new)
        toolbar.addAction(new_btn)

        open_btn = QAction("Відкрити", self)
        open_btn.triggered.connect(self.action_open)
        toolbar.addAction(open_btn)

        stats_btn = QAction("Статистика", self)
        stats_btn.triggered.connect(self.action_stats)
        toolbar.addAction(stats_btn)

    def _create_statusbar(self):
        self.statusBar().showMessage("Готово до роботи")

    def _connect_signals(self):
        self.text_edit.textChanged.connect(self._update_char_count)

    def _update_char_count(self):
        text = self.text_edit.toPlainText()
        char_count = len(text)
        word_count = len(text.split()) if text.strip() else 0
        self.statusBar().showMessage(
            f"Символів: {char_count} | Слів: {word_count}"
        )

    def action_new(self):
        self.text_edit.clear()
        self.statusBar().showMessage("Створено новий документ")

    def action_open(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Відкрити файл", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_edit.setPlainText(content)
                self.statusBar().showMessage(f"Відкрито: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Не вдалося відкрити файл:\n{e}")

    def action_about(self):
        QMessageBox.about(
            self,
            "Про програму",
            "Текстовий редактор\nЛабораторна робота №4\nСтворено з використанням PyQt6"
        )

    def action_stats(self):
        text = self.text_edit.toPlainText()
        char_count = len(text)
        word_count = len(text.split()) if text.strip() else 0
        line_count = text.count("\n") + 1 if text else 0
        QMessageBox.information(
            self,
            "Статистика",
            f"Символів: {char_count}\nСлів: {word_count}\nРядків: {line_count}"
        )


def main():
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
