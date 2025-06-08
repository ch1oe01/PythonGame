# 匯入自訂基底類別與必要模組
from gobject import GameObject
from pathlib import Path
import pygame
import math

# 敵人子彈類別，繼承 GameObject
class EnemyBullet(GameObject):
    def __init__(self, xy, playground, sensitivity):
        super().__init__(playground)  # 呼叫父類別，傳入遊戲場地尺寸

        # 設定圖片路徑，並載入敵人子彈圖檔
        path = Path(__file__).parents[1] / 'res' / 'enemy_bullet.png'
        self._image = pygame.image.load(str(path)).convert_alpha()  # 支援透明背景
        self._image = pygame.transform.scale(self._image, (20, 40))  # 縮小為 20x40 像素
        self.image = self._image  # 提供外部參考用

        # 初始位置：來自外部 xy 參數（通常為敵人中心）
        self._x, self._y = xy

        # 子彈速度設定（向下移動）
        self._moveScale = 0.5 * sensitivity

        # 子彈可活動邊界（超出就消失）
        self._objectBound = (
            0,                    # 最小 X（左界）
            self._playground[0],  # 最大 X（畫面寬度）
            0,                    # 最小 Y（上界）
            self._playground[1]   # 最大 Y（畫面高度）
        )

        self.available = True     # 子彈是否仍存在（True 則會繪製與移動）
        self.collided = False     # 是否碰撞過（避免重複處理）

        # 設定碰撞半徑：用圖片寬度的一半當作圓形範圍
        self._radius = self._image.get_width() / 2

    # 每一幀更新子彈狀態
    def update(self):
        self._y += self._moveScale  # 子彈往下移動（敵人攻擊玩家）

        # 超出畫面底部則標記為無效（不再處理與繪製）
        if self._y > self._objectBound[3]:
            self.available = False

        # 更新子彈中心點座標（供碰撞使用）
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )
