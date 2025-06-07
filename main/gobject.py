import math

class GameObject:
    def __init__(self, playground=None):
        # 初始化遊戲物件的基本屬性
        if playground is None:
            self._playground = [1200, 900]  # 預設場地大小
        else:
            self._playground = playground  # 自定場地大小

        # 物件活動的邊界範圍（left, right, top, bottom）
        self._objectBound = (0, self._playground[0], 0, self._playground[1])

        # 座標與移動向量
        self._changeX = 0
        self._changeY = 0
        self._x = 0
        self._y = 0
        self._moveScale = 1  # 速度倍率

        self._hp = 1  # 預設生命值
        self._image = None  # 圖像物件
        self._available = True  # 是否有效（例如已爆炸就失效）
        self._center = None  # 中心座標（用於碰撞）
        self._radius = 0     # 半徑（碰撞範圍）
        self._collided = False  # 是否發生碰撞

    # 各種屬性的 getter/setter
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

    # 移動相關方法
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
        # 移動更新位置
        self._x += self._changeX
        self._y += self._changeY

        # 邊界限制判斷
        if self._x > self._objectBound[1]:
            self._x = self._objectBound[1]
        if self._x < self._objectBound[0]:
            self._x = self._objectBound[0]

        if self._y > self._objectBound[3]:
            self._y = self._objectBound[3]
        if self._y < self._objectBound[2]:
            self._y = self._objectBound[2]

        # 更新中心點座標（給碰撞判斷用）
        if self._image:
            self._center = (
                self._x + self._image.get_rect().w / 2,
                self._y + self._image.get_rect().h / 2
            )

    # 碰撞偵測（圓形碰撞方式）
    def _collided_(self, it):
        if self._center is None or it.center is None:
            return False  # 防止 None 引發錯誤
        if self._radius is None or it.radius is None:
            return False

        # 計算兩中心距離
        distance = math.hypot(
            self._center[0] - it.center[0],
            self._center[1] - it.center[1]
        )

        # 判斷是否碰撞（兩圓相交）
        return distance < (self._radius + it.radius)
