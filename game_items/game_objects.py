from game_items.game_arguments import *
import pickle
import os
import settings
import pygame
import math


def get_unique_id():
    if os.path.exists("game_items/last_id.pickle"):
        last_id = -1
        with open("game_items/last_id.pickle", "rb") as f:
            last_id = pickle.load(f)
        last_id += 1
        with open("game_items/last_id.pickle", "wb") as f:
            pickle.dump(last_id, f)
        return last_id
    else:
        last_id = 0
        with open("game_items/last_id.pickle", "wb") as f:
            pickle.dump(last_id, f)
        return last_id


def _set_last_id(new_id):
    with open("game_items/last_id.pickle", "wb") as f:
        pickle.dump(new_id, f)


class GameObject:
    args = {"name": StrArgument(), "id": LabelArgument(), "x": IntArgument(), "y": IntArgument(),
            "width": IntArgument(is_positive=True), "height": IntArgument(is_positive=True), "image_name": StrArgument(editor_name="Image path"),
            "layer": IntArgument()}

    def __init__(self, name: str, x: int, y: int, w: int, h: int, image_name: str, layer: int = 0) -> None:
        self._id: int = get_unique_id()
        self._name = name
        self._x = x
        self._y = y
        self._width = w
        self._height = h
        self._image_name = image_name
        self._layer = layer
        self._angle = 0
        self.angle = self.angle

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    @property
    def id(self):
        return self._id

    def _set_new_unick_id(self):
        self._id = get_unique_id()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, n):
        self._x = n

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, n):
        self._y = n

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, n):
        self._width = n

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, n):
        self._height = n

    @property
    def image_name(self):
        return self._image_name

    @image_name.setter
    def image_name(self, n):
        self._image_name = n

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, n):
        self._layer = n

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, n):
        self._angle = n % 360
        if self._angle < 0:
            self._angle += 360

    def move(self, x, y):
        self.x += x
        self.y += y

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, a):
        self.angle += a

    def set_rotate(self, a):
        self.a = a

    def move_direction(self, direction):
        x += math.cos(direction / (360 / (math.pi * 2)))
        y += math.sin(direction / (360 / (math.pi * 2)))

    def move_forward(self):
        x += math.cos(self.angle / (360 / (math.pi * 2)))
        y += math.sin(self.angle / (360 / (math.pi * 2)))

    def update(self):
        pass

    def pygame_draw(self, screen, camera):
        image = pygame.image.load(self.image_name)
        image = pygame.transform.rotate(image, self.angle - 90)
        image = pygame.transform.scale(image, (self.width, self.height))
        screen.blit(image, (settings.screen_x // 2 + camera.pos_x + self.x - self.width // 2,
                            settings.screen_y // 2 + camera.pos_y - self.y - self.height // 2))


SAMPLE_GAME_OBJECT = GameObject(
    "GameObject", 0, 0, 100, 100, "content/images/knight.jpg")
