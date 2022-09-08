from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


HELP = '''Help:
Управление в эдиторе:
        w - вверх          r - масштаб +
    a - влево d - вправо   
        s - вниз           f - масштаб -
        
    Левая кнопка мышки - перемещение объектов
     и камеры.
     
     ctrl - для выбора нескольких оюъектов
     

     
Коллекция спрайтов (нижняя панель)

Правая кнопка мыши открывает меню.'''


class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setBaseSize(1000, 2000)
        self.setWindowTitle("OpenLewelEditor - Help")
        self.box = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.help_label = QLabel()
        self.help_label.setText(HELP)
        self.scroll_area.setWidget(self.help_label)

        self.box.addWidget(self.scroll_area)

        self.setLayout(self.box)
        self.show()
