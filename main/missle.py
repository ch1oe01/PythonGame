# 匯入必要模組與基礎類別
import pygame.image
from gobject import GameObject
from pathlib import Path

# 定義玩家子彈類別，繼承自 GameObject
class MyMissile(GameObject):
    def __init__(self, playground, xy, sensitivity=1):
        super().__init__(playground)  # 呼叫父類別初始化（給 playground 尺寸）

        # 定義圖片路徑
        __parent_path = Path(__file__).parents[1]
        self.__missile_path = __parent_path / 'res' / 'missile-removebg-preview.png'

        # 載入子彈圖並保留透明通道
        self._image = pygame.image.load(self.__missile_path).convert_alpha()
        self.image = self._image  # 提供外部使用的圖像屬性

        # 取得圖片寬高
        missile_w = self._image.get_rect().w
        missile_h = self._image.get_rect().h

        # 設定初始位置：以 xy 為中心微調
        self._x = xy[0] - (missile_w // 2) + 10  # 向左偏移以對齊機翼
        self._y = xy[1]

        # 設定碰撞半徑（寬度一半）
        self._radius = missile_w / 2

        # 設定飛彈的移動速度（向上）
        self._moveScale = 0.7 * sensitivity

        # 設定飛彈活動邊界（超出上方就會無效）
        self._objectBound = (
            0,                             # 左邊界
            self._playground[0],           # 右邊界（畫面寬度）
            -missile_h - 10,               # 上邊界（超出視窗即無效）
            self._playground[1]            # 下邊界（其實用不到）
        )

        # 子彈初始狀態（可用且未碰撞）
        self.available = True
        self.collided = False

        # 飛彈啟動後自動向上移動
        self.to_the_top()

        # 計算初始中心點，用於碰撞判斷
        self._center = (
            self._x + missile_w / 2,
            self._y + missile_h / 2
        )

    # 設定飛彈為「向上移動」
    def to_the_top(self):
        self._changeX = 0
        self._changeY = -self._moveScale  # Y 軸向上是負數

    # 每幀更新一次飛彈的位置與狀態
    def update(self):
        self._y += self._changeY  # 向上移動

        # 如果超出畫面上方，則將其標記為無效
        if self._y < self._objectBound[2]:
            self.available = False

        # 更新中心點位置（用於碰撞）
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )

    # 子彈與敵人的碰撞偵測
    def collision_detect(self, enemies):
        for e in enemies:
            if self._collided_(e):  # 若發生碰撞
                self.collided = True       # 子彈標記為已碰撞
                self.available = False     # 子彈設為不可用（等同刪除）
                e.collided = True          # 敵人也標記為碰撞
                e.available = False        # 敵人被摧毀，設為不可用
