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
            self._y = xy[1]import pygame
import math
from pathlib import Path

class GameObject:
    def __init__(self, playground=None):
        if playground is None:
            self._playground = [1200, 900]
        else:
            self._playground = playground

        self._objectBound = (0, self._playground[0], 0, self._playground[1])
        self._changeX = 0
        self._changeY = 0
        self._x = 0
        self._y = 0
        self._moveScale = 1
        self._hp = 1
        self._image = None
        self._available = True
        self._center = None
        self._radius = 0
        self._collided = False

    @property
    def xy(self):
        return self._x, self._y

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        self._available = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = value

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def collided(self):
        return self._collided

    @collided.setter
    def collided(self, value):
        self._collided = value

    def to_the_left(self):
        self._changeX = -self._moveScale

    def to_the_right(self):
        self._changeX = self._moveScale

    def to_the_bottom(self):
        self._changeY = self._moveScale

    def to_the_top(self):
        self._changeY = -self._moveScale

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

        if self._image:
            self._center = (
                self._x + self._image.get_rect().w / 2,
                self._y + self._image.get_rect().h / 2
            )
            self._radius = self._image.get_rect().w / 2

    def _collided_(self, it):
        if self._center is None or it.center is None:
            return False
        if self._radius is None or it.radius is None:
            return False

        distance = math.hypot(self._center[0] - it.center[0], self._center[1] - it.center[1])
        return distance < (self._radius + it.radius)

    def collision_detect(self, targets):
        for target in targets:
            if self._collided_(target):
                self.collided = True
                target.collided = True
                self.available = False
                target.available = False
                return True
        return False

class EnemyBullet(GameObject):
    def __init__(self, xy, playground, sensitivity):
        super().__init__(playground)
        bullet_path = Path(__file__).parents[1] / 'res' / 'enemy_bullet.png'
        self._image = pygame.image.load(str(bullet_path)).convert_alpha()
        self._image = pygame.transform.scale(self._image, (20, 40))
        self._x, self._y = xy
        self._moveScale = sensitivity

    def update(self):
        self._y += self._moveScale * 0.5
        if self._y > self._playground[1]:
            self.available = False
        if self._image:
            self._center = (
                self._x + self._image.get_rect().w / 2,
                self._y + self._image.get_rect().h / 2
            )
            self._radius = self._image.get_rect().w / 2


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