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


        missile_w = self._image.get_rect().w
        missile_h = self._image.get_rect().h

        # 設定初始位置
        self._x = xy[0] - (missile_w // 2) - 12
        self._y = xy[1]

        # 設定碰撞半徑與移動速度
        self._radius = missile_w / 2
        self._moveScale = 0.7 * sensitivity

        # 定義子彈的可移動邊界（超出上邊界就會消失）
        self._objectBound = (
            0,                             # 最小 x
            self._playground[0],           # 最大 x（畫面寬度）
            -missile_h - 10,               # 最小 y（超出上邊界）
            self._playground[1]            # 最大 y（畫面高度）
        )

        # 狀態標記：是否碰撞
        self.available = True
        self.collided = False

        # 飛彈預設往上移動
        self.to_the_top()

        # 計算初始中心點位置
        self._center = (
            self._x + missile_w / 2,
            self._y + missile_h / 2
        )

    def to_the_top(self):
        # 設定飛彈向上移動
        self._changeX = 0
        self._changeY = -self._moveScale

    def update(self):
        # 每幀更新 y 座標（向上移動）
        self._y += self._changeY

        # 若超出上邊界則設為無效
        if self._y < self._objectBound[2]:
            self.available = False

        # 更新中心點座標
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )

    def collision_detect(self, enemies):
        # 與敵人列表逐一檢查碰撞
        for e in enemies:
            if self._collided_(e):
                # 若碰撞到，雙方皆設為碰撞與無效
                self.collided = True
                self.available = False
                e.collided = True
                e.available = False
