from gobject import GameObject
from pathlib import Path
import pygame
import math
import random
from enemy_bullet import EnemyBullet

class Enemy(GameObject):
    def __init__(self, playground=None, xy=None, sensitivity=1):
        GameObject.__init__(self, playground)
        self._moveScale = 0.15 * sensitivity    # 移動速度

        __parent_path = Path(__file__).parents[1]
        self.__enemy_path = __parent_path / 'res' / 'enemy-removebg-preview.png'
        self._image = pygame.image.load(self.__enemy_path)
        self.image = self._image

        # 計算碰撞半徑（用於圓形碰撞判斷）
        self._radius = 0.3 * math.hypot(
            self._image.get_rect().w, self._image.get_rect().h)

        # 如果沒指定位置就隨機從畫面頂端生成
        if xy is None:
            self._x = random.randint(10, playground[0] - 103)  # 保留邊界
            self._y = -113  # 在畫面頂部之外出現
        else:
            self._x = xy[0]
            self._y = xy[1]

        # 移動邊界限制（避免超出畫面）
        self._objectBound = (
            10,
            self._playground[0] - 103,
            -113,
            self._playground[1]
        )

        # 隨機決定初始斜率方向（左上或右上斜飛）
        if random.random() > 0.5:
            self._slope = 0.5
        else:
            self._slope = -0.5

        # 根據斜率計算 X 與 Y 軸移動量
        self._moveScaleX = math.sin(self._slope * math.pi / 2) * self._moveScale
        self._moveScaleY = math.cos(self._slope * math.pi / 2) * self._moveScale

        self.to_the_bottom()  # 初始化為向下飛行

    def to_the_bottom(self):
        # 設定移動方向向下（有斜率會斜移）
        self._changeY = self._moveScaleY
        self._changeX = self._moveScaleX

    def update(self):
        # 每幀更新位置
        self._x += self._changeX
        self._y += self._changeY

        # 有小機率隨機改變斜率方向（左右來回）
        if random.random() < 0.001:
            self._slope = -self._slope
            self._changeX = math.sin(self._slope * math.pi / 2) * self._moveScale

        # 碰到左右邊界反彈
        if self._x > self._objectBound[1]:
            self._x = self._objectBound[1]
            self._slope = -self._slope
            self._changeX = math.sin(self._slope * math.pi / 2) * self._moveScale
        if self._x < self._objectBound[0]:
            self._x = self._objectBound[0]
            self._slope = -self._slope
            self._changeX = math.sin(self._slope * math.pi / 2) * self._moveScale

        # 超出畫面底部就設為無效（消失）
        if self._y > self._objectBound[3]:
            self._y = self._objectBound[3]
            self._available = False

        # 超出畫面上方則限制位置（避免往上飛）
        if self._y < self._objectBound[2]:
            self._y = self._objectBound[2]

        # 更新中心點座標
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )

    def fire(self):
        # 敵人子彈從中心底部發射
        bullet_x = self._x + self._image.get_width() // 2
        bullet_y = self._y + self._image.get_height()
        return EnemyBullet((bullet_x, bullet_y), self._playground, self._moveScale * 10)
