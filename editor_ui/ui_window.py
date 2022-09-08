from editor_ui.ui_editor import LevelEditor
from editor_ui.ui_constructor import UiConstructor
from editor_ui.ui_collection import UiCollection
from editor_ui.ui_listing import UiListing
from editor_ui.ui_settings import SettingsWindow
from editor_ui.ui_help import HelpWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from editor_ui.ui_scheme import *
import copy

from game_items.game_base import GameBase


class EditorWindow(QMainWindow):
    def __init__(self, base: GameBase):
        super().__init__()
        self.base = base
        self._color_scheme = ColorSheme()
        self.setWindowTitle(f"OpenLewelEditor - {base.base_name}")
        self._create_actions()

        self.editor = LevelEditor(self)
        self.setCentralWidget(self.editor)

        self.menu = EditorMenu([self.new_bd_action, self.open_bd_action, self.new_col_action, self.open_col_action, self.append_collection_action], [self.open_settings_action, self.delete_gm_action, self.copy_gm_action,
                               self.cut_gm_action, self.paste_gm_action], [self.open_help_action])
        self.setMenuBar(self.menu)

        self.constructor = UiConstructor(self)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.constructor)

        self.collection = UiCollection(self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.collection)

        self.tools = UiTools(self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tools)

        self.listing = UiListing(self)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.listing)

        self.update_color_schene()

        self.show()

    @property
    def game_base(self):
        return self.base

    @property
    def color_scheme(self):
        return self._color_scheme

    def _get_editor(self):
        return self.editor

    def _create_actions(self):
        self.delete_gm_action = QAction("Delete")
        self.delete_gm_action.triggered.connect(self._delete_gm)
        self.delete_gm_action.setShortcuts(["Ctrl+Shift+D", "Delete"])

        self.copy_gm_action = QAction("Copy")
        self.copy_gm_action.triggered.connect(self._copy_gm)
        self.copy_gm_action.setShortcut("Ctrl+Shift+C")

        self.cut_gm_action = QAction("Cut")
        self.cut_gm_action.triggered.connect(self._cut_gm)
        self.cut_gm_action.setShortcut("Ctrl+Shift+X")

        self.paste_gm_action = QAction("Paste")
        self.paste_gm_action.triggered.connect(self._paste_gm)
        self.paste_gm_action.setShortcut("Ctrl+Shift+V")

        self.open_settings_action = QAction("Settings")
        self.open_settings_action.triggered.connect(self._open_settings)

        self.open_help_action = QAction("Help")
        self.open_help_action.triggered.connect(self._open_help)

        self.open_bd_action = QAction("Open base")
        self.open_bd_action.triggered.connect(self._open_bd)

        self.new_bd_action = QAction("New base")
        self.new_bd_action.triggered.connect(self._new_bd)

        self.open_col_action = QAction("Open collection")
        self.open_col_action.triggered.connect(self._open_collection)

        self.new_col_action = QAction("New collection")
        self.new_col_action.triggered.connect(self._new_collection)

        self.append_collection_action = QAction("Append collection")
        self.append_collection_action.triggered.connect(
            self._append_collection)

    def update_color_schene(self):
        pass

    def _delete_gm(self):
        if self.base.target is None:
            return
        self.base.remove_game_objects(*self.base.target)
        self.base.target = []
        self.update_targeted_widgets()

    def _copy_gm(self):
        if len(self.base.target) <= 0:
            return
        self.base.bufer = []
        for gm in self.base.target:
            g = copy.copy(gm)
            g._set_new_unick_id()
            self.base.bufer.append(g)
        self.update_targeted_widgets()

    def _cut_gm(self):
        if len(self.base.target) <= 0:
            return
        self.base.bufer = []
        for g in self.base.target:
            self.base.bufer.append(g)
            self.base.remove_game_objects(g)
        self.base.target = []
        self.update_targeted_widgets()

    def _paste_gm(self):
        if self.base.bufer is None:
            return
        self.base.add_game_objects(*self.base.bufer)
        g = copy.copy(self.base.bufer)
        g._set_new_unick_id()
        self.base.bufer = g
        self.update_targeted_widgets()

    def _open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.exec()
        self.update_color_schene()

    def _open_help(self):
        help_window = HelpWindow()
        help_window.exec()

    def _open_bd(self):
        export_file_name = QFileDialog.getOpenFileName(
            self, "Export data base", "content/bases/", "*.bd")

        print("Open", export_file_name)

        if export_file_name == ("", ""):
            return

        col_name = self.base.collection_name
        self.base.exit()
        self.base = GameBase(export_file_name[0], col_name)
        self.setWindowTitle(f"OpenLewelEditor - {self.base.base_name}")
        self.update_targeted_widgets()
        self.update_collection()
        self.update()

    def _new_bd(self):
        new_bd_name = QFileDialog.getSaveFileName(self,
                                                  "New data base", "content/bases/", "*.bd")

        print("New", new_bd_name)

        if new_bd_name == ("", ""):
            return

        col_name = self.base.collection_name
        self.base.exit()
        self.base = GameBase(new_bd_name[0], col_name)
        self.setWindowTitle(f"OpenLewelEditor - {self.base.base_name}")
        self.update_targeted_widgets()
        self.update_collection()
        self.update()

    def _open_collection(self):
        export_file_name = QFileDialog.getOpenFileName(
            self, "Export collection", "content/bases/", "*.bd")

        print("Open col", export_file_name)

        if export_file_name == ("", ""):
            return

        base_name = self.base.base_name
        self.base.exit()
        self.base = GameBase(base_name, export_file_name[0])
        self.setWindowTitle(f"OpenLewelEditor - {self.base.base_name}")
        self.update_targeted_widgets()
        self.update_collection()
        self.update()

    def _new_collection(self):
        new_col_name = QFileDialog.getSaveFileName(self,
                                                   "New collection", "content/bases/", "*.bd")

        print("New col", new_col_name)

        if new_col_name == ("", ""):
            return

        base_name = self.base.base_name
        self.base.exit()
        self.base = GameBase(base_name, new_col_name[0])
        self.setWindowTitle(f"OpenLewelEditor - {self.base.base_name}")
        self.update_targeted_widgets()
        self.update_collection()
        self.update()

    def _append_collection(self):
        export_file_name = QFileDialog.getOpenFileName(
            self, "Export data base", "content/bases/", "*.bd")

        print("Append", export_file_name)

        if export_file_name == ("", ""):
            return

        self.append_base = GameBase(export_file_name[0])

        for g in self.append_base.collection:
            f = self.base.find_game_object_from_id(g.id)
            if f is not None:
                g._set_new_unick_id()
            self.base.add_collection_game_objects(g)

        self.append_base.exit()

        self.update_collection()
        self.update()

    def update_targeted_widgets(self):
        self.constructor.update_constructor()
        self.editor.update()
        self.listing.update_scroll_area()

    def update_editor(self):
        self.editor.update()

    def update_collection(self):
        self.collection.update_collection()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # TODO: перенести эту функцию в editor
        # TODO: оставить пользователям заметку, что загружать
        # чужие бд вообщето не безопасно
        if event.key() == Qt.Key.Key_S:
            self.editor.move_camera(0, -3)
        if event.key() == Qt.Key.Key_W:
            self.editor.move_camera(0, 3)
        if event.key() == Qt.Key.Key_D:
            self.editor.move_camera(3, 0)
        if event.key() == Qt.Key.Key_A:
            self.editor.move_camera(-3, 0)
        if event.key() == Qt.Key.Key_R:
            self.editor.move_scale(1.01)
        if event.key() == Qt.Key.Key_F:
            self.editor.move_scale(0.99)


class EditorMenu(QMenuBar):
    def __init__(self, file_actions, editor_actions, other_action):
        super().__init__()
        self.file_menu = QMenu("File")
        self.file_menu.addActions(file_actions)
        self.addMenu(self.file_menu)

        self.editor_menu = QMenu("Editor")
        self.editor_menu.addActions(editor_actions)
        self.addMenu(self.editor_menu)

        # self.help_menu = QMenu("Help")
        # self.help_menu.addActions(help_actions)
        # self.addMenu(self.help_menu)

        self.addActions(other_action)


class UiTools(QToolBar):
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.magnet_button = QCheckBox()
        self.magnet_button.setText("magnet move")
        self.magnet_button.pressed.connect(self.set_magneted)
        self.addWidget(self.magnet_button)

    def set_magneted(self):
        if not self.magnet_button.isChecked():
            self.window._get_editor().set_magnet(True)
        else:
            self.window._get_editor().set_magnet(False)
