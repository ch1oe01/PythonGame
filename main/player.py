from gobject import GameObject
from pathlib import Path
import pygame
import math

class Player(GameObject):
    def __init__(self, playground, xy=None, sensitivity=1):
        super().__init__(playground)
        self._moveScale = 0.8 * sensitivity  # 移動速度設定

        __parent_path = Path(__file__).parents[1]
        self.__player_path = __parent_path / 'res' / 'airplane.png'

        self._image = pygame.image.load(self.__player_path).convert_alpha()
        self.image = self._image

        # 初始位置與中心點設定
        self._x = 0
        self._y = 0
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )

        # 設定碰撞半徑（取圖片對角線的 30%）
        self._radius = 0.3 * math.hypot(self._image.get_rect().w, self._image.get_rect().h)
        self._changeX = 0
        self._changeY = 0

        # 設定初始位置（預設在畫面底部中央）
        if xy is None:
            self._x = (self._playground[0] - self._image.get_rect().w) / 2
            self._y = 3 * self._playground[1] / 4
        else:
            self._x = xy[0]
            self._y = xy[1]

        # 設定移動邊界（上下左右 10px 邊界）
        self._objectBound = (
            10,
            self._playground[0] - self._image.get_rect().w - 10,
            10,
            self._playground[1] - self._image.get_rect().h - 10
        )

    # 四個方向的移動設定
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

        # 左右邊界限制
        if self._x > self._objectBound[1]:
            self._x = self._objectBound[1]
        if self._x < self._objectBound[0]:
            self._x = self._objectBound[0]

        # 更新中心點座標
        if self._y > self._objectBound[3]:
            self._y = self._objectBound[3]
        if self._y < self._objectBound[2]:
            self._y = self._objectBound[2]

        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )

    # 玩家偵測與敵人的碰撞
    def collision_detect(self, enemies):
        for m in enemies:
            if self._collided_(m):
                self._hp -= 10
                self._collided = True
                m.hp = -1
                m.collided = True
                m.available = False
