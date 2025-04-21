from gobject import GameObject
from pathlib import Path
import pygame
import random


class Explosion(GameObject):
    explosion_effect = []

    def __init__(self, xy=None):
        GameObject.__init__(self)
        if xy is None:
            self._x = random.randint(10, self._playground[0]-103)
            self._y = -113
        else:
            self._x = xy[0]
            self._y = xy[1]

        if Explosion.explosion_effect:
            pass
        else:
            __parent_path = Path(__file__).parents[1]
            icon_path = __parent_path/'res'/'explosion_small-removebg-preview.png'
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent_path / 'res' / 'explosion_medium-removebg-preview.png'
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent_path / 'res' / 'explosion_large.png'
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent_path / 'res' / 'explosion_medium-removebg-preview.png'
            Explosion.explosion_effect.append(pygame.image.load(icon_path))
            icon_path = __parent_path / 'res' / 'explosion_small-removebg-preview.png'
            Explosion.explosion_effect.append(pygame.image.load(icon_path))

        self.__image_index = 0
        self._image = Explosion.explosion_effect[self.__image_index]
        self.__fps_count = 0

    def update(self):
        self.__fps_count += 1
        if self.__fps_count > 30:
            self.__image_index += 1
            if self.__image_index > 4:
                self._available = False
            else:
                self._image = Explosion.explosion_effect[self.__image_index]
