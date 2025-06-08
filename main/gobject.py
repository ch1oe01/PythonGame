import math

# 遊戲中所有物件的基底類別，提供共通屬性與方法
class GameObject:
    def __init__(self, playground=None):
        # 設定遊戲場地大小（用於碰撞與邊界判斷）
        if playground is None:
            self._playground = [1200, 900]  # 預設場地為 1200x900
        else:
            self._playground = playground  # 可自定大小傳入

        # 設定活動邊界（左、右、上、下）
        self._objectBound = (
            0,
            self._playground[0],
            0,
            self._playground[1]
        )

        # 基本屬性初始化
        self._changeX = 0       # X 軸移動量
        self._changeY = 0       # Y 軸移動量
        self._x = 0             # 物件左上角 X 座標
        self._y = 0             # 物件左上角 Y 座標
        self._moveScale = 1     # 移動倍率（速度）

        self._hp = 1            # 預設生命值（子彈用不到，玩家與敵人可用）
        self._image = None      # 圖片物件
        self._available = True  # 是否有效（False 表示已被摧毀或離場）
        self._center = None     # 中心點（用於碰撞計算）
        self._radius = 0        # 圓形碰撞半徑
        self._collided = False  # 是否發生碰撞

    # 座標與狀態屬性存取（用 property 提供統一介面）

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

    # 🎮 移動控制方法（由外部呼叫）
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

    # 每幀更新座標與中心點
    def update(self):
        self._x += self._changeX
        self._y += self._changeY

        # 邊界限制：防止物件跑出場地外
        if self._x > self._objectBound[1]:
            self._x = self._objectBound[1]
        if self._x < self._objectBound[0]:
            self._x = self._objectBound[0]

        if self._y > self._objectBound[3]:
            self._y = self._objectBound[3]
        if self._y < self._objectBound[2]:
            self._y = self._objectBound[2]

        # 若有圖片，計算中心點座標（用於圓形碰撞）
        if self._image:
            self._center = (
                self._x + self._image.get_rect().w / 2,
                self._y + self._image.get_rect().h / 2
            )

    # 圓形碰撞判斷函數
    def _collided_(self, it):
        # 若中心點或半徑為 None，則不執行碰撞
        if self._center is None or it.center is None:
            return False
        if self._radius is None or it.radius is None:
            return False

        # 計算兩物件中心點的距離
        distance = math.hypot(
            self._center[0] - it.center[0],
            self._center[1] - it.center[1]
        )

        # 判斷是否碰撞：兩個圓的半徑和大於距離即碰撞
        return distance < (self._radius + it.radius)
