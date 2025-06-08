# 匯入必要模組與自訂基底類別
from gobject import GameObject
from pathlib import Path
import pygame
import math
import random
from enemy_bullet import EnemyBullet  # 敵人子彈類別

# 定義敵人類別，繼承自 GameObject
class Enemy(GameObject):
    def __init__(self, playground=None, xy=None, sensitivity=1):
        GameObject.__init__(self, playground)  # 呼叫父類別，設定 playground 尺寸

        self._moveScale = 0.2 * sensitivity  # 敵人移動速度倍率

        # 載入敵人圖片資源
        __parent_path = Path(__file__).parents[1]
        self.__enemy_path = __parent_path / 'res' / 'enemy-removebg-preview.png'
        self._image = pygame.image.load(self.__enemy_path)
        self.image = self._image  # 提供外部呼叫用

        # 計算碰撞半徑：敵人圖片的對角線 × 0.3（用於圓形碰撞）
        self._radius = 0.3 * math.hypot(
            self._image.get_rect().w,
            self._image.get_rect().h
        )

        # 設定初始位置：隨機從畫面頂部生成，若 xy 參數為空
        if xy is None:
            self._x = random.randint(10, playground[0] - 103)  # 隨機 X 座標，避免靠邊
            self._y = -113  # 超出畫面頂部，用來從上方滑入
        else:
            self._x = xy[0]
            self._y = xy[1]

        # 移動邊界（限制敵人活動範圍）
        self._objectBound = (
            10,
            self._playground[0] - 103,  # 限制右邊界
            -113,
            self._playground[1]        # 底部就是畫面高度
        )

        # 決定初始斜率方向（左右其中一邊）
        if random.random() > 0.5:
            self._slope = 0.5
        else:
            self._slope = -0.5

        # 計算根據斜率的 X/Y 每幀移動量（向下 + 斜移）
        self._moveScaleX = math.sin(self._slope * math.pi / 2) * self._moveScale
        self._moveScaleY = math.cos(self._slope * math.pi / 2) * self._moveScale

        # 初始化移動方向為向下（帶斜率）
        self.to_the_bottom()

    def to_the_bottom(self):
        # 設定移動向量為向下滑動（含左右斜移）
        self._changeY = self._moveScaleY
        self._changeX = self._moveScaleX

    def update(self):
        # 每幀更新敵人位置
        self._x += self._changeX
        self._y += self._changeY

        # 小機率隨機改變斜率方向（左右來回飄移）
        if random.random() < 0.001:
            self._slope = -self._slope
            self._changeX = math.sin(self._slope * math.pi / 2) * self._moveScale

        # 碰到右邊界就反彈回左邊
        if self._x > self._objectBound[1]:
            self._x = self._objectBound[1]
            self._slope = -self._slope
            self._changeX = math.sin(self._slope * math.pi / 2) * self._moveScale

        # 碰到左邊界就反彈回右邊
        if self._x < self._objectBound[0]:
            self._x = self._objectBound[0]
            self._slope = -self._slope
            self._changeX = math.sin(self._slope * math.pi / 2) * self._moveScale

        # 敵人超出畫面底部則視為無效（清除）
        if self._y > self._objectBound[3]:
            self._y = self._objectBound[3]
            self._available = False

        # 超出上方邊界時強制調整位置（避免飛出去）
        if self._y < self._objectBound[2]:
            self._y = self._objectBound[2]

        # 更新中心點位置（用於碰撞計算）
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )

    def fire(self):
        # 敵人發射子彈：從圖片底部中心發射
        bullet_x = self._x + self._image.get_width() // 2
        bullet_y = self._y + self._image.get_height()
        return EnemyBullet(
            (bullet_x, bullet_y),                   # 發射位置
            self._playground,                       # 遊戲範圍
            self._moveScale * 10                    # 子彈速度
        )
