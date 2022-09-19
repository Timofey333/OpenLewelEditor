from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import json


class SettingsWindow(QDialog):
    def __init__(self, window):
        super().__init__()
        self.setBaseSize(300, 300)
        self.setWindowTitle("OpenLewelEditor - Settings")
        self.window = window
        self.settings = {}
        with open("editor_ui/editor_settings.json", "r") as file:
            self.settings = json.load(file)
        self.schemes = {}
        with open("editor_ui/color_schemes.json") as file:
            self.schemes = json.load(file)
        self.box = QVBoxLayout()

        self.tile_name_label = QLabel()
        self.tile_name_label.setText("Tile: ")
        self.box.addWidget(self.tile_name_label)
        self.tile_editor = QLineEdit()
        self.tile_editor.setText(str(self.settings["tile"]))
        self.box.addWidget(self.tile_editor)

        # TODO: сделать цветовые схемы
        self.schemes_name_label = QLabel()
        self.schemes_name_label.setText("Color scheme: ")
        self.box.addWidget(self.schemes_name_label)

        with open("editor_ui/color_schemes.json", "r") as file:
            schemes = json.load(file)

        with open("editor_ui/editor_settings.json", "r") as file:
            settings = json.load(file)

        self.schemes_combo = QComboBox()
        for i, _ in self.schemes.items():
            if i == "target":
                continue
            self.schemes_combo.addItem(i)
        self.schemes_combo.setCurrentIndex(
            list(schemes.keys()).index(settings["color_scheme"]))
        self.box.addWidget(self.schemes_combo)

        self.box.addWidget(QWidget(), 10)

        self.accept_button = QPushButton()
        self.accept_button.setText("Accept")
        self.accept_button.pressed.connect(self.accept_settings)
        self.box.addWidget(self.accept_button)

        self.setLayout(self.box)
        self.show()

    def accept_settings(self):
        if not self.set_settings():
            error_window = ErrorWindow()
            error_window.exec()
        else:
            self.window._get_editor().set_settings()
            self.window.update_color_schene()
            self.window.update()

    def set_settings(self):
        if not self.tile_editor.text().isdigit():
            return False
        if int(self.tile_editor.text()) == 0:
            return False
        self.settings["tile"] = int(self.tile_editor.text())
        self.settings["color_scheme"] = self.schemes_combo.itemText(
            self.schemes_combo.currentIndex())
        with open("editor_ui/editor_settings.json", "w") as file:
            json.dump(self.settings, file)

        return True


class ErrorWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setBaseSize(100, 50)
        self.setWindowTitle("Error")
        self.box = QVBoxLayout()

        self.label = QLabel()
        self.label.setText("Error")
        self.box.addWidget(self.label)

        self.setLayout(self.box)
