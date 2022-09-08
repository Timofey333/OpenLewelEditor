from xml.sax.handler import property_declaration_handler
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from game_items.game_base import GameBase
from game_items.game_objects import GameObject
import json
from editor_ui.ui_scheme import *


class LevelEditor(QWidget):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.scale = 1
        self.tile = 50
        self.camera_y = 0
        self.camera_x = 0

        self.is_magnet = False

        self.set_settings()

    @property
    def base(self):
        return self.window.game_base

    @property
    def color_scheme(self) -> ColorSheme:
        return self.window.color_scheme

    def set_magnet(self, n):
        self.is_magnet = n

    def move_camera(self, x: int, y: int):
        self.camera_x += x
        self.camera_y += y
        self.update()

    def set_camera_pos(self, x: int, y: int):
        self.camera_x = x
        self.camera_y = y
        self.update()

    @property
    def camera_pos(self):
        return self.camera_x, self.camera_y

    def move_scale(self, n):
        self.scale *= n
        self.update()

    def set_settings(self):
        settings = {}
        with open("editor_ui/editor_settings.json", "r") as file:
            settings = json.load(file)
        self.tile = settings["tile"]

    def paintEvent(self, event: QPaintEvent) -> None:
        scale = self.scale
        tile = self.tile
        camera_x, camera_y = self.camera_x, self.camera_y
        width, height = self.width(), self.height()
        qp = QPainter(self)
        # qp.setBrush(QBrush(QColor(self.color_scheme.editor_fon)))
        qp.drawRect(QRect(0, 0, self.width(), self.height()))
        qp.setPen(QPen(QColor(self.color_scheme.editor_lines),
                  1, Qt.PenStyle.SolidLine))
        for y in range(- tile, int((height + tile) / scale), tile):
            line_y = int((y + camera_y % tile) * scale +
                         (height // 2) % (tile * scale))
            qp.drawLine(0, line_y, width, line_y)
            qp.drawText(5, line_y, str(
                int(- y + self.tile_rounding(camera_y, scaled=False) + self.tile_rounding((height / scale) / 2, scaled=False))))
        for x in range(-tile, int((width + tile) / scale), tile):
            line_x = int((x - camera_x % tile) * scale +
                         (width // 2) % (tile * scale))
            qp.drawLine(line_x, 0, line_x, height)
            qp.drawText(line_x, height - 10,
                        str(int(x + self.tile_rounding(camera_x, scaled=False) - self.tile_rounding((width / scale) / 2, scaled=False))))
        qp.setPen(QPen(QColor(self.color_scheme.editor_text),
                  1, Qt.PenStyle.SolidLine))
        qp.drawText(width - 100, 15, str(f"tile: {tile} scale: {scale}"))
        target_id = list(map(lambda g: g.id, self.base.target))
        for g in sorted(self.base.game_objects, key=lambda g: g.layer):
            image = QImage(g.image_name)
            gx, gy = self.base_to_widget_pos(g.x, g.y)
            if image.isNull():
                qp.setPen(QPen(QColor(self.color_scheme.editor_error),
                          3, Qt.PenStyle.SolidLine))
                qp.drawRect(QRectF(gx - g.width // 2 * scale, gy -
                                   g.height // 2 * scale, g.width * scale, g.height * scale))
            else:
                qp.drawImage(QRectF(gx - g.width // 2 * scale, gy -
                             g.height // 2 * scale, g.width * scale, g.height * scale), image)
            if g.id in target_id:
                qp.setPen(
                    QPen(QColor(self.color_scheme.editor_target), 3, Qt.PenStyle.SolidLine))
                qp.drawRect(QRectF(gx - g.width // 2 * scale, gy -
                                   g.height // 2 * scale, g.width * scale, g.height * scale))

    def tile_rounding(self, n, scaled=True):
        if not scaled:
            return (n // self.tile) * self.tile
        return (n // (self.tile * self.scale)) * (self.tile * self.scale)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            if len(self.base.target) == 0:
                mouse_widget_x, mouse_widget_y = event.point(
                    0).position().x(), event.point(0).position().y()
                mouse_x, mouse_y = self.widget_to_base_pos(
                    mouse_widget_x, mouse_widget_y)
                mouse_start_move_x, mouse_start_move_y = self.mouse_start_move_pos
                self.set_camera_pos(int(self.camera_x + mouse_start_move_x - mouse_x),
                                    int(self.camera_y + mouse_start_move_y - mouse_y))
                self.update()
            elif len(self.base.target) == 1:
                mouse_widget_x, mouse_widget_y = event.point(
                    0).position().x(), event.point(0).position().y()
                mouse_x, mouse_y = self.widget_to_base_pos(
                    mouse_widget_x, mouse_widget_y)
                mouse_start_move_x, mouse_start_move_y = self.mouse_start_move_pos
                if self.is_magnet:
                    self.base.target[0].x, self.base.target[0].y = (int(self.tile_rounding(mouse_x)),
                                                                    int(self.tile_rounding(mouse_y)))
                else:
                    self.base.target[0].x, self.base.target[0].y = (int(mouse_x),
                                                                    int(mouse_y))
                self.update()
            else:
                mouse_widget_x, mouse_widget_y = event.point(
                    0).position().x(), event.point(0).position().y()
                mouse_x, mouse_y = self.widget_to_base_pos(
                    mouse_widget_x, mouse_widget_y)
                mouse_start_move_x, mouse_start_move_y = self.mouse_start_move_pos
                for i in range(len(self.base.target)):
                    g = self.base.target[i]
                    shift_x, shift_y = self.target_x_shift[i], self.target_y_shift[i]
                    if self.is_magnet:
                        g.x, g.y = (int(self.tile_rounding(mouse_x - shift_x)),
                                    int(self.tile_rounding(mouse_y - shift_y)))
                    else:
                        g.x, g.y = (int(mouse_x - shift_x),
                                    int(mouse_y - shift_y))
                self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            mouse_widget_x, mouse_widget_y = event.point(
                0).position().x(), event.point(0).position().y()
            self.mouse_start_move_pos = self.widget_to_base_pos(
                mouse_widget_x, mouse_widget_y)
            p = self.point_object(
                *self.mouse_start_move_pos)
            if p is not None:
                if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                    if p not in self.base.target:
                        self.base.target.append(p)
                    self.target_x_shift, self.target_y_shift = [], []
                    for g in self.base.target:
                        self.target_x_shift.append(
                            - g.x + self.mouse_start_move_pos[0])
                        self.target_y_shift.append(
                            - g.y + self.mouse_start_move_pos[1])
                else:
                    self.base.target = [p]
            else:
                self.base.target = []
            self.window.update_targeted_widgets()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if len(self.base.target) != 0:
            self.base.update_game_objects(*self.base.target)
            self.window.update_targeted_widgets()

    def point_object(self, base_point_x, base_point_y) -> GameObject or None:
        x, y = base_point_x, base_point_y
        for g in sorted(self.base.game_objects, key=lambda g: g.layer, reverse=True):
            g_left, g_right = g.x - g.width // 2, g.x + g.width // 2
            g_up, g_down = g.y + g.height // 2, g.y - g.height // 2
            if (g_left <= x <= g_right) and (g_down <= y <= g_up):
                return g
        return None

    def widget_to_base_pos(self, widget_x, widget_y):
        return int(self.camera_x + (widget_x - self.width() // 2) / self.scale), \
            int(self.camera_y + (- widget_y + self.height() // 2) / self.scale)

    def base_to_widget_pos(self, base_x, base_y):
        scale = self.scale
        camera_x, camera_y = self.camera_x, self.camera_y
        width, height = self.width(), self.height()
        nx = int((- camera_x + base_x) * scale + width / 2)
        ny = int((camera_y - base_y) * scale + height / 2)
        return nx, ny
