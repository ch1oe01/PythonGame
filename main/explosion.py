from gobject import GameObject
from pathlib import Path
import pygame
import random

class Explosion(GameObject):
    # 靜態變數：共用的爆炸動畫圖片陣列，只載入一次
    explosion_effect = []

    def __init__(self, xy=None):
        super().__init__()

        # 爆炸產生位置：預設從上方隨機生成，或使用傳入座標
        if xy is None:
            self._x = random.randint(10, self._playground[0] - 103)
            self._y = -113
        else:
            self._x = xy[0]
            self._y = xy[1]

        # 如果還沒載入爆炸圖片，就初始化靜態動畫素材
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

        # 設定初始動畫影格
        self.__image_index = 0
        self._image = Explosion.explosion_effect[self.__image_index]
        self.image = self._image

        # 控制動畫速度（FPS計數器）
        self.__fps_count = 0

        # 遊戲物件狀態設定
        self.available = True
        self.collided = False
        self._radius = 0  # 爆炸動畫不用碰撞判斷

        # 中心點設定（動畫播放位置基準）
        self._center = (
            self._x + self._image.get_rect().w / 2,
            self._y + self._image.get_rect().h / 2
        )

    def update(self):
        # 每幀更新：每隔一定時間切換下一張爆炸圖
        self.__fps_count += 1
        if self.__fps_count > 30:
            self.__image_index += 1
            self.__fps_count = 0  # 重設計數器
            if self.__image_index > 4:
                self.available = False  # 所有動畫圖播完，標記為無效
            else:
                # 切換到下一張動畫圖
                self._image = Explosion.explosion_effect[self.__image_index]
                self.image = self._image
