from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from game_items.game_collection import GameCollection
from game_items.game_base import GameBase
import copy
from game_items.game_objects import GameObject


class UpdateScrollBarThreas(QThread):
    mysignal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        self.mysignal.emit()


class UiCollection(QToolBar):
    def __init__(self, window):
        super().__init__()
        self.setMinimumHeight(180)
        self._window = window
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_cont = QWidget()
        self.scroll_cont.setLayout(QVBoxLayout())
        self.scroll_area.setWidget(self.scroll_cont)
        self.addWidget(self.scroll_area)
        self.update_collection()

    @property
    def window(self):
        return self._window

    @property
    def base(self):
        return self.window.game_base

    def update_collection(self):
        self.update_thread = UpdateScrollBarThreas()
        self.update_thread.mysignal.connect(self._update_collection)
        self.update_thread.start()

    def _update_collection(self):
        self.scroll_box = QHBoxLayout()
        # widgets
        for g in self.base.collection:
            w = GameObjectCollectionWidget(self, g)
            self.scroll_box.addWidget(w)
        self.scroll_cont = QWidget()
        self.scroll_cont.setLayout(self.scroll_box)
        self.scroll_area.setWidget(self.scroll_cont)
        self.update()

    def get_scroll_box(self):
        return self.scroll_box


class GameObjectCollectionWidget(QWidget):
    def __init__(self, collection, game_object):
        super().__init__()
        self.collection = collection
        self.game_obejct = game_object
        self._create_actions()
        self.menu_actions = [self.create_gm_action, self.remove_gm_action]
        self._create_context_menu()

        self.box = QVBoxLayout()

        self.name_label = QLabel()
        self.name_label.setText(game_object.name)
        self.box.addWidget(self.name_label)

        self.image_label = QLabel()
        self.pixmap = QPixmap(game_object.image_name)
        self.pixmap = self.pixmap.scaled(100, 100)
        self.image_label.setPixmap(self.pixmap)
        self.box.addWidget(self.image_label)

        self.setLayout(self.box)

    def _create_actions(self):
        self.create_gm_action = QAction("Create")
        self.create_gm_action.triggered.connect(self._create_gm)

        self.remove_gm_action = QAction("Remove")
        self.remove_gm_action.triggered.connect(self._remove_gm)

    def _create_gm(self):
        g: GameObject = copy.copy(self.game_obejct)
        g._set_new_unick_id()
        new_x, new_y = self.collection.window._get_editor().camera_pos
        g.x = new_x
        g.y = new_y
        self.collection.window.game_base.add_game_objects(g)
        # self.collection.window.update_collection()

    def _remove_gm(self):
        if len(self.collection.window.game_base.collection_list) <= 1:
            return
        self.collection.window.game_base.remove_collection_game_object(
            self.game_obejct)
        self.collection.update_collection()

    def _create_context_menu(self):
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        for a in self.menu_actions:
            self.addAction(a)

    def eventFilter(self, object: 'QObject', event: 'QEvent') -> bool:
        if event.type() == QEvent.MouseButtonPress:
            mouse_event = QMouseEvent(event)
            if mouse_event.button == Qt.MouseButton.RightButton:
                pass
        return super().eventFilter(object, event)
