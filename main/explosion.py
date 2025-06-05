from gobject import GameObject
from pathlib import Path
import pygame
import random


class Explosion(GameObject):
    explosion_effect = []

    def __init__(self, xy=None):
        super().__init__()
        if xy is None:
            self._x = random.randint(10, self._playground[0] - 103)
            self._y = -113
        else:
            self._x = xy[0]
            self._y = xy[1]

        if not Explosion.explosion_effect:
            __parent_path = Path(__file__).parents[1]
            Explosion.explosion_effect.append(
                pygame.image.load(__parent_path / 'res' / 'explosion_small-removebg-preview.png').convert_alpha())
            Explosion.explosion_effect.append(
                pygame.image.load(__parent_path / 'res' / 'explosion_medium-removebg-preview.png').convert_alpha())
            Explosion.explosion_effect.append(
                pygame.image.load(__parent_path / 'res' / 'explosion_large.png').convert_alpha())
            Explosion.explosion_effect.append(
                pygame.image.load(__parent_path / 'res' / 'explosion_medium-removebg-preview.png').convert_alpha())
            Explosion.explosion_effect.append(
                pygame.image.load(__parent_path / 'res' / 'explosion_small-removebg-preview.png').convert_alpha())

        self.__image_index = 0
        self._image = Explosion.explosion_effect[self.__image_index]
        self.image = self._image  # ✅ 主程式會用的圖
        self.__fps_count = 0

        self.available = True   # ✅ 主程式需要這個屬性
        self.collided = False   # ✅ 安全統一
        self._radius = 0        # ✅ 沒用到也要設，防止錯誤
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )

    def update(self):
        self.__fps_count += 1
        if self.__fps_count > 30:
            self.__image_index += 1
            if self.__image_index > 4:
                self.available = False  # ✅ 正確屬性
            else:
                self._image = Explosion.explosion_effect[self.__image_index]
                self.image = self._image  # ✅ 更新對外圖
