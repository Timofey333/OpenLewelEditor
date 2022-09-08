from PyQt6.QtWidgets import QApplication
from game_items.game_base import GameBase
from editor_ui.ui_window import EditorWindow
import sys
from game_items.game_objects import GameObject


def main():
    app = QApplication(sys.argv)
    base = GameBase("content/bases/new_base.bd",
                    "content/bases/new_collection.bd")
    print(base.game_objects)
    window = EditorWindow(base)
    print("Start app")
    app.exec()
    window.game_base.exit()
    print("Stop app")


main()
