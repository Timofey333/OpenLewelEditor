from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class LabelArgument:
    def __init__(self, editor_name=None) -> None:
        self.edirot_name = editor_name

    def get_widget(self, constructor, game_object, argument_name):
        return LabelArgumentWidget(constructor, game_object, argument_name, editor_name=self.edirot_name)


class LabelArgumentWidget(QWidget):
    def __init__(self, constructor, game_object, parameter_name, editor_name) -> None:
        super().__init__()
        self._editor_name = editor_name
        self.game_object = game_object
        self.parameter_name = parameter_name
        self.constructor = constructor
        self._build()
        self.update_widget()

    def _build(self):
        self.box = QHBoxLayout()

        self.name_label = QLabel()
        self.box.addWidget(self.name_label)

        self.setLayout(self.box)

    @property
    def name_widget(self):
        return self.name_label

    @property
    def editor_widget(self):
        return None

    @property
    def editor_name(self):
        if self._editor_name is None:
            return self.parameter_name.capitalize()
        return self._editor_name.capitalize()

    def update_widget(self):
        print(self.game_object.id)
        self.name_label.setText(
            self.editor_name + ": " + eval(f"str(game_object.{self.parameter_name})", {"game_object": self.game_object}))
        self.update()

    def get(self):
        return None


class StrArgument:
    def __init__(self, editor_name=None):
        self.edirot_name = editor_name

    def get_widget(self, constructor, game_object, argument_name):
        return StrArgumentWidget(constructor, game_object, argument_name, editor_name=self.edirot_name)


class StrArgumentWidget(LabelArgumentWidget):
    def __init__(self, constructor, game_object, parameter_name, editor_name) -> None:
        super().__init__(constructor, game_object, parameter_name, editor_name)

    def _build(self):
        super()._build()
        self.editor = QLineEdit()
        self.box.addWidget(self.editor)

    @property
    def editor_widget(self):
        return self.editor

    def update_widget(self):
        self.name_label.setText(self.editor_name + ": ")
        self.editor_widget.setText(
            eval(f"str(game_object.{self.parameter_name})", {"game_object": self.game_object}))
        self.editor_widget.textEdited.connect(self.update_argument)

    def get(self):
        return self.editor_widget.text()

    def update_argument(self):
        new_value = self.get()
        exec(f"game_object.{self.parameter_name} = get()",
             {"game_object": self.game_object, "get": self.get})
        self.constructor.update_game_objects(self.game_object)


class IntArgument(StrArgument):
    def __init__(self, editor_name=None, null_value=0, is_positive=False):
        self.editor_name = editor_name
        self.is_positive = is_positive
        self.null_value = null_value

    def get_widget(self, constructor, game_object, argument_name):
        return IntArgumentWidget(constructor, game_object, argument_name, self.editor_name, self.null_value, self.is_positive)


class IntArgumentWidget(StrArgumentWidget):
    def __init__(self, constructor, game_object, parameter_name, editor_name, null_value=0, is_positive=False) -> None:
        self.is_positive = is_positive
        self.null_value = null_value
        super().__init__(constructor, game_object, parameter_name, editor_name)

    def get(self):
        return int(super().get())

    def update_widget(self):
        result = super().update_widget()
        self.filter_editor_widger()
        return result

    def update_argument(self):
        self.filter_editor_widger()
        return super().update_argument()

    def filter_editor_widger(self):
        new_number = ""
        is_first_for_null = True
        is_first_for_minus = True
        for e in self.editor_widget.text():
            if e.isdigit():
                if e == "0" and is_first_for_null:
                    continue
                new_number += e
                is_first_for_null = False
                is_first_for_minus = False
            elif e == "-":
                if is_first_for_minus and not self.is_positive:
                    new_number += e
                    is_first_for_minus = False
        if new_number == "":
            new_number = str(self.null_value)
        if new_number == "-":
            new_number = "-0"
        self.editor_widget.setText(new_number)
