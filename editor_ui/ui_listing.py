from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from game_items.game_base import GameBase


class UiListing(QToolBar):
    def __init__(self, window):
        super().__init__()
        self._window = window

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.addWidget(self.scroll_area)
        self.update_scroll_area()

    @property
    def window(self):
        return self._window

    def update_scroll_area(self):
        self.scroll_cont = QWidget()
        self.scroll_box = QVBoxLayout()
        for g in self.window.game_base.game_objects:
            w = GameObjectListingWidget(self, g)
            self.scroll_box.addWidget(w)
        self.scroll_cont.setLayout(self.scroll_box)
        self.scroll_area.setWidget(self.scroll_cont)
        self.update()


class GameObjectListingWidget(QPushButton):
    def __init__(self, listing, game_object) -> None:
        super().__init__()
        self.listing = listing
        self.game_object = game_object
        # self.box = QHBoxLayout()

        # self.name = QLabel()
        # self.name.setText(game_object.name)
        # self.box.addWidget(self.name)

        # self.setLayout(self.box)
        self.setText(game_object.name)
        self.pressed.connect(self.set_target)

    def set_target(self) -> None:
        self.listing.window.game_base.target = [self.game_object]
        self.listing.window.update_targeted_widgets()
