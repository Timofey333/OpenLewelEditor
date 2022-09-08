import pygame
import settings


class Log:
    def __init__(self, log=["The log."]):
        self.log = log
        self._font = settings.pygame_ui_font

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, n):
        self._font = n

    def error(self, s: str):
        self.log.append(s)
        print(s)

    def draw(self, screen, color=(0, 0, 0)):
        text_surf = self.font.render(self.log[-1], 1, color)
        screen.blit(text_surf, (30, settings.screen_y - 30))
