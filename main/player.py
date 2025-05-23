from gobject import GameObject
from pathlib import Path
from typing import Union
from pygame.surface import Surface, SurfaceType
import pygame
import math

class Player(GameObject):
    def __init__(self, playground, xy=None, sensitivity=1):
        GameObject.__init__(self, playground)
        self._moveScale = 0.5 * sensitivity
        __parent_path = Path(__file__).parents[1]
        self.__player_path = __parent_path / 'res' / 'airplaneicon-removebg-preview.png'

        # 載入圖片
        self._image = pygame.image.load(self.__player_path)

        # 縮小圖片
        original_size = self._image.get_size()
        scale_factor = 0.5  # 設定縮小比例
        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
        self._image = pygame.transform.scale(self._image, new_size)

        self._x = 0
        self._y = 0
        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2
        self._radius = 0.3 * math.hypot(self._image.get_rect().w, self._image.get_rect().h)
        self._changeX = 0
        self._changeY = 0

        if xy is None:
            self._x = (self._playground[0] - self._image.get_rect().w) / 2
            self._y = 3 * self._playground[1] / 4
        else:
            self._x = xy[0]
            self._y = xy[1]

        self._objectBound = (
            10,
            self._playground[0] - self._image.get_rect().w - 10,
            10,
            self._playground[1] - self._image.get_rect().h - 10
        )

    def to_the_left(self):
        self._changeX = -self._moveScale

    def to_the_right(self):
        self._changeX = self._moveScale

    def to_the_top(self):
        self._changeY = -self._moveScale

    def to_the_bottom(self):
        self._changeY = self._moveScale

    def stop_x(self):
        self._changeX = 0

    def stop_y(self):
        self._changeY = 0

    def update(self):
        self._x += self._changeX
        self._y += self._changeY

        if self._x > self._objectBound[1]:
            self._x = self._objectBound[1]
        if self._x < self._objectBound[0]:
            self._x = self._objectBound[0]

        if self._y > self._objectBound[3]:
            self._y = self._objectBound[3]
        if self._y < self._objectBound[2]:
            self._y = self._objectBound[2]

        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2

    def collision_detect(self, enemies):
        for m in enemies:
            if self._collided_(m):
                self._hp -= 10
                self._collided = True
                m.hp = -1
                m.collided = True
                m.available = False
