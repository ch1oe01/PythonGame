# 匯入基底類別 GameObject 與相關模組
from gobject import GameObject
from pathlib import Path
import pygame
import math

# 定義玩家類別，繼承自 GameObject
class Player(GameObject):
    def __init__(self, playground, xy=None, sensitivity=1):
        super().__init__(playground)  # 呼叫父類別初始化，並設置 playground 大小

        self._moveScale = 0.8 * sensitivity  # 玩家移動速度倍率，根據 sensitivity 控制快慢

        # 設定圖片路徑
        __parent_path = Path(__file__).parents[1]
        self.__player_path = __parent_path / 'res' / 'airplane.png'

        # 載入玩家飛機圖片（含透明通道）
        self._image = pygame.image.load(self.__player_path).convert_alpha()
        self.image = self._image  # 給 GameObject 使用

        # 預設初始位置與中心點（暫時為 0,0，後續會被更新）
        self._x = 0
        self._y = 0
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )

        # 計算碰撞半徑：飛機圖片對角線長度的 30%
        self._radius = 0.3 * math.hypot(
            self._image.get_rect().w, self._image.get_rect().h
        )

        # 初始移動向量（預設不移動）
        self._changeX = 0
        self._changeY = 0

        # 如果沒有指定座標 xy，則預設置於畫面底部中央
        if xy is None:
            self._x = (self._playground[0] - self._image.get_rect().w) / 2
            self._y = 3 * self._playground[1] / 4
        else:
            self._x = xy[0]
            self._y = xy[1]

        # 設定邊界限制（上下左右保留 10 px，不可超出畫面）
        self._objectBound = (
            10,
            self._playground[0] - self._image.get_rect().w - 10,
            10,
            self._playground[1] - self._image.get_rect().h - 10
        )

    # 以下為四個方向的移動控制函數（由主程式呼叫）
    def to_the_left(self):
        self._changeX = -self._moveScale  # 向左移動

    def to_the_right(self):
        self._changeX = self._moveScale  # 向右移動

    def to_the_top(self):
        self._changeY = -self._moveScale  # 向上移動

    def to_the_bottom(self):
        self._changeY = self._moveScale  # 向下移動

    def stop_x(self):
        self._changeX = 0  # 停止 X 軸移動

    def stop_y(self):
        self._changeY = 0  # 停止 Y 軸移動

    # 每一幀更新位置
    def update(self):
        self._x += self._changeX
        self._y += self._changeY

        # 限制 X 軸不超出邊界
        if self._x > self._objectBound[1]:
            self._x = self._objectBound[1]
        if self._x < self._objectBound[0]:
            self._x = self._objectBound[0]

        # 限制 Y 軸不超出邊界
        if self._y > self._objectBound[3]:
            self._y = self._objectBound[3]
        if self._y < self._objectBound[2]:
            self._y = self._objectBound[2]

        # 更新中心點座標（用於碰撞計算）
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )

    # 玩家與敵人清單進行碰撞偵測（呼叫於主程式內）
    def collision_detect(self, enemies):
        for m in enemies:
            if self._collided_(m):  # 若玩家與敵人發生碰撞
                self._hp -= 10          # 玩家 HP 扣 10
                self._collided = True   # 玩家被擊中狀態
                m.hp = -1               # 敵人標記為已死（如果有用到）
                m.collided = True       # 敵人已碰撞標記
                m.available = False     # 敵人將在下一幀被清除
