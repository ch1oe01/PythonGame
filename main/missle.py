import pygame.image
from gobject import GameObject
from pathlib import Path

class MyMissile(GameObject):
    def __init__(self, playground, xy, sensitivity=1):
        super().__init__(playground)
        __parent_path = Path(__file__).parents[1]
        self.__missile_path = __parent_path / 'res' / 'missile-removebg-preview.png'
        self._image = pygame.image.load(self.__missile_path).convert_alpha()
        self.image = self._image

        # ✅ 自動置中子彈（傳入 xy = 飛機中心）
        missile_w = self._image.get_rect().w
        missile_h = self._image.get_rect().h
        self._x = xy[0] - (missile_w // 2)-12
        self._y = xy[1]

        self._radius = missile_w / 2
        self._moveScale = 0.7 * sensitivity

        self._objectBound = (
            0,
            self._playground[0],
            -missile_h - 10,
            self._playground[1]
        )

        self.available = True
        self.collided = False
        self.to_the_top()

        self._center = (
            self._x + missile_w / 2,
            self._y + missile_h / 2
        )

    def to_the_top(self):
        self._changeX = 0
        self._changeY = -self._moveScale

    def update(self):
        self._y += self._changeY
        if self._y < self._objectBound[2]:
            self.available = False
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )

    def collision_detect(self, enemies):
        for e in enemies:
            if self._collided_(e):
                self.collided = True
                self.available = False
                e.collided = True
                e.available = False
