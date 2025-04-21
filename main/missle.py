import pygame.image

from gobject import GameObject
from pathlib import Path


class MyMissile(GameObject):
    def __init__(self, playground, xy, sensitivity=1):
        GameObject.__init__(self, playground)
        __parent_path = Path(__file__).parents[1]
        self.__missile_path = __parent_path/'res'/'missile-removebg-preview.png'
        self._image = pygame.image.load(self.__missile_path)
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().h/2
        self._radius = self._image.get_rect().w/2
        self._x = xy[0]
        self._y = xy[1]

        self._objectBound = (0, self._playground[0],
                             -self._image.get_rect().h-10, self._playground[1])
        self._moveScale = 0.7*sensitivity
        self.to_the_top()

    def __del__(self):
        print(self.__class__.__name__, "Missile is being automatically destroyed")

    def update(self):
        self._y += self._changeY
        if self._y < self._objectBound[2]:
            self._available = False
        self._center = self._x + self._image.get_rect().w/2, self._y + self._image.get_rect().w/2

    def collision_detect(self, enemies):
        for m in enemies:
            if self._collided_(m):
                self._hp -= 10
                self._collided = True
                self._available = False
                m.hp = -1
                m.collided = True
                m.available = False
