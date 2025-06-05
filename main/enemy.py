from gobject import GameObject
from pathlib import Path
import pygame
import math
import random

class Enemy(GameObject):
    def __init__(self, playground=None, xy=None, sensitivity=1):
        super().__init__(playground)
        self._moveScale = 0.1 * sensitivity
        __parent_path = Path(__file__).parents[1]
        self.__enemy_path = __parent_path / 'res' / 'enemy-removebg-preview.png'
        self._image = pygame.image.load(self.__enemy_path).convert_alpha()
        self.image = self._image
        self._radius = 0.3 * math.hypot(self._image.get_rect().w, self._image.get_rect().h)

        if xy is None:
            self._x = random.randint(10, playground[0] - 103)
            self._y = -113  # 從畫面上方生成
        else:
            self._x = xy[0]
            self._y = xy[1]

        self._objectBound = (10, self._playground[0] - 103,
                             -113, self._playground[1])

        # 左右移動初始方向
        if random.random() > 0.5:
            self._slope = 0.5
        else:
            self._slope = -0.5

        self._moveScaleX = math.sin(self._slope * math.pi / 2) * self._moveScale
        self._moveScaleY = math.cos(self._slope * math.pi / 2) * self._moveScale

        self.to_the_bottom()

        # ✅ 加入缺少的重要屬性
        self.available = True
        self.collided = False

    def to_the_bottom(self):
        self._changeY = self._moveScaleY
        self._changeX = self._moveScaleX

    def update(self):
        self._x += self._changeX
        self._y += self._changeY

        # 隨機改變方向
        if random.random() < 0.001:
            self._slope = -self._slope
            self._changeX = math.sin(self._slope * math.pi / 2) * self._moveScale

        # 碰到邊界反彈
        if self._x > self._objectBound[1]:
            self._x = self._objectBound[1]
            self._slope = -self._slope
            self._changeX = math.sin(self._slope * math.pi / 2) * self._moveScale
        if self._x < self._objectBound[0]:
            self._x = self._objectBound[0]
            self._slope = -self._slope
            self._changeX = math.sin(self._slope * math.pi / 2) * self._moveScale

        # 超出畫面底部則消失
        if self._y > self._objectBound[3]:
            self.available = False  # ✅ 正確設為無效
        if self._y < self._objectBound[2]:
            self._y = self._objectBound[2]

        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2
