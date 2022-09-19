import pygame
from game_items.game_objects import GameObject
from game_items.game_base import GameBase
from pygame_game.camera import Camera
from pygame_game.log import Log


class Map(pygame.sprite.Group):
    def __init__(self, file_name: str) -> None:
        super().__init__()
        self.file_name = file_name
        self.base = GameBase(file_name, file_name)
        self.objects = self.base.game_objects
        self.base.exit()
        self.camera = Camera(self, 0, 0)
        self._log = Log()

    @property
    def log(self):
        return self._log

    def add_object(self, object: GameObject):
        self.objects.append(object)

    def set_camera(self, camera: Camera):
        self.camera = camera

    @property
    def game_objects(self) -> list[GameObject]:
        return self.objects

    def draw(self, screen):
        for d in sorted(self.game_objects, key=lambda g: g.layer):
            d.pygame_draw(screen, self.camera)

    def update(self):
        for g in self.game_objects:
            g.update()
