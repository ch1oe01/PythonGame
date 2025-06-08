# 匯入基礎類別與模組
from gobject import GameObject
from pathlib import Path
import pygame
import random

# 爆炸動畫物件類別（不會互動、不會移動，只會播放動畫後消失）
class Explosion(GameObject):
    # 靜態變數：只載入一次爆炸圖片，供所有爆炸物件共用
    explosion_effect = []

    def __init__(self, xy=None):
        super().__init__()  # 初始化基底屬性

        # 爆炸出現位置（若無指定，則隨機從畫面上方生成）
        if xy is None:
            self._x = random.randint(10, self._playground[0] - 103)
            self._y = -113
        else:
            self._x = xy[0]
            self._y = xy[1]

        # 載入爆炸動畫素材（靜態共用，只載入一次）
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

        # 初始動畫影格索引
        self.__image_index = 0
        self._image = Explosion.explosion_effect[self.__image_index]
        self.image = self._image  # 提供外部畫面繪製使用

        # 用來控制動畫切換速度的計數器
        self.__fps_count = 0

        # 狀態標記：有效與否、是否碰撞（動畫不需偵測碰撞）
        self.available = True
        self.collided = False
        self._radius = 0  # 不需碰撞判斷

        # 中心點設定，用於正確顯示動畫（以中心為基準）
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )

    # 每幀更新動畫狀態
    def update(self):
        self.__fps_count += 1  # 每幀遞增 FPS 計數器

        if self.__fps_count > 30:
            self.__image_index += 1  # 換下一張圖
            self.__fps_count = 0     # 重設計數器

            # 如果所有影格播完，設定為不可用（將從畫面移除）
            if self.__image_index > 4:
                self.available = False
            else:
                # 切換到下一張爆炸圖像
                self._image = Explosion.explosion_effect[self.__image_index]
                self.image = self._image
