from threading import Thread
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from game_items.game_objects import GameObject
import copy


class UiConstructor(QToolBar):

    window = None

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setMinimumWidth(200)

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.addWidget(self.scroll_area)
        self.update_constructor()

    @property
    def color_scheme(self):
        return self.window.color_scheme

    def update_constructor(self):
        self.scroll_box = QVBoxLayout()
        # add widgets
        target_game_objects = self.window.game_base.target
        if len(target_game_objects) == 1:
            target_game_object = target_game_objects[0]
            self.label = QLabel()
            self.label.setText(target_game_object.name)
            self.scroll_box.addWidget(self.label)

            self.arg_widgets = []
            for name, argument in target_game_object.__class__.args.items():
                arg_widget = argument.get_widget(
                    self, target_game_object, name)
                self.arg_widgets.append(arg_widget)
                self.scroll_box.addWidget(arg_widget)

            self.add_to_collection_button = QPushButton()
            self.add_to_collection_button.setText("Add to collection")
            self.add_to_collection_button.pressed.connect(
                self.add_to_collection)
            self.scroll_box.addWidget(self.add_to_collection_button)

        self.scroll_cont = QWidget()
        self.scroll_cont.setLayout(self.scroll_box)
        self.scroll_area.setWidget(self.scroll_cont)
        self.update()

    def add_to_collection(self):
        if len(self.window.game_base.target) == 1:
            g: GameObject = copy.copy(self.window.game_base.target[0])
            g._set_new_unick_id()
            self.window.game_base.add_collection_game_objects(g)
            self.window.update_collection()

    def update_game_objects(self, game_object):
        self.window.game_base.update_game_objects(game_object)
        self.window.update_editor()
