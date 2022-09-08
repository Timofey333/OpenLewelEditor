from pygame_game.map import Map
from game_items.game_objects import GameObject
from pygame_game.camera import Camera
import settings
import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode(
        (settings.screen_x, settings.screen_y))
    time = pygame.time.Clock()

    map = Map("new_base.bd")

    camera = Camera(map, 0, 0)
    map.set_camera(camera)

    running = True
    while running:
        time.tick(settings.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        map.update()

        screen.fill("#ffffff")
        map.draw(screen)

        map.log.draw(screen)

        pygame.display.flip()
    # to do: сохранение
    pygame.quit()


main()
