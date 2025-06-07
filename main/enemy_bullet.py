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

        # 設定初始位置為傳入座標 xy
        self._x, self._y = xy

        # 子彈移動速度（向下移動）
        self._moveScale = 0.2 * sensitivity

        # 子彈可移動的邊界限制（畫面範圍內）
        self._objectBound = (
            0,
            self._playground[0],   # 畫面寬度
            0,
            self._playground[1]    # 畫面高度
        )

        self.available = True     # 判斷子彈是否仍有效（可顯示）
        self.collided = False     # 是否已碰撞
        self._radius = self._image.get_width() / 2  # 碰撞半徑（用於圓形碰撞）

    def update(self):
        # 子彈每幀向下移動
        self._y += self._moveScale

        # 如果超出畫面底部，就設為無效
        if self._y > self._objectBound[3]:
            self.available = False

        # 更新子彈中心點座標（用於碰撞檢查）
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )
