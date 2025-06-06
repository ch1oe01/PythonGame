from gobject import GameObject
from pathlib import Path
import pygame
import math

class EnemyBullet(GameObject):
    def __init__(self, xy, playground, sensitivity):
        super().__init__(playground)
        path = Path(__file__).parents[1] / 'res' / 'enemy_bullet.png'
        self._image = pygame.image.load(str(path)).convert_alpha()
        self._image = pygame.transform.scale(self._image, (20, 40))
        self.image = self._image

        self._x, self._y = xy
        self._moveScale = 0.3 * sensitivity
        self._objectBound = (0, self._playground[0], 0, self._playground[1])
        self.available = True
        self.collided = False
        self._radius = self._image.get_width() / 2

    def update(self):
        self._y += self._moveScale
        if self._y > self._objectBound[3]:
            self.available = False

        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )
