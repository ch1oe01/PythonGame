import pygame
import random
from pathlib import Path

# 匯入自訂類別：玩家、飛彈、敵人、爆炸、敵人子彈、基底物件
from player import Player
from missle import MyMissile
from enemy import Enemy
from explosion import Explosion
from enemy_bullet import EnemyBullet
from gobject import GameObject

def main():
    # 設定資源資料夾的路徑
    parent_path = Path(__file__).parents[1]
    image_path = parent_path / 'res'
    icon_path = image_path / 'airplaneicon.png'
    font_path = str(image_path / 'msjh.ttc')
    bg_path = image_path / 'background.png'
    cover_path = image_path / 'cover_image.png'

    # 初始化 pygame 與音效模組
    pygame.init()
    pygame.mixer.init()

    # 畫面尺寸與遊戲區域（畫面高度已改為 600）
    screenHigh = 600
    screenWidth = 1200
    playground = [screenWidth, screenHigh]

    # 載入爆炸音效
    explosion1 = pygame.mixer.Sound(str(image_path / 'explosion1.mp3'))

    # 建立視窗
    screen = pygame.display.set_mode((screenWidth, screenHigh))
    pygame.display.set_caption("射擊遊戲")
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    # 載入背景與封面圖片，並縮放成全螢幕大小
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (screenWidth, screenHigh))
    cover_bg = pygame.image.load(cover_path).convert()
    cover_bg = pygame.transform.scale(cover_bg, (screenWidth, screenHigh))

    # 載入字型（分為標準字、標題字、血量字）
    font = pygame.font.Font(font_path, 40)
    title_font = pygame.font.SysFont("Microsoft JhengHei", 80, bold=True)
    hp_font = pygame.font.SysFont("Microsoft JhengHei", 24, bold=True)

    # 設定遊戲更新率與角色移動速度倍率
    fps = 120
    clock = pygame.time.Clock()
    movingScale = 500 / fps

    # 建立玩家角色，並設定初始血量
    player = Player(playground=playground, sensitivity=movingScale)
    player._hp = 100

    # 控制移動方向的計數（防止多重輸入問題）
    keyCountX = 0
    keyCountY = 0

    # 建立遊戲物件清單
    Missiles = []      # 玩家子彈列表
    Enemies = []       # 敵人列表
    Boom = []          # 爆炸效果列表
    EnemyBullets = []  # 敵人子彈列表

    # 自訂事件（子彈連發、產生敵人）
    launchMissile = pygame.USEREVENT + 1
    createEnemy = pygame.USEREVENT + 2
    pygame.time.set_timer(createEnemy, 500)  # 每 500 毫秒產生一隻敵人

    # 設定初始分數與最高分
    score = 0
    high_score = 0

    # 遊戲狀態：主選單、遊戲中、暫停、結束
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    game_state = MENU

    running = True  # 控制遊戲主迴圈

    while running:
        dt = clock.tick(fps)  # 每幀執行間隔
        screen.fill((0, 0, 0))  # 清空畫面背景

        # 處理事件（鍵盤、滑鼠、退出等）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 主選單狀態處理
            if game_state == MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # 開始新遊戲
                        game_state = PLAYING
                        Missiles.clear()
                        Enemies.clear()
                        Boom.clear()
                        EnemyBullets.clear()
                        score = 0
                        player = Player(playground=playground, sensitivity=movingScale)
                        player._hp = 100
                        keyCountX = 0
                        keyCountY = 0
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            # 遊戲進行中處理玩家輸入
            elif game_state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        keyCountX += 1
                        player.to_the_left()
                    elif event.key == pygame.K_d:
                        keyCountX += 1
                        player.to_the_right()
                    elif event.key == pygame.K_s:
                        keyCountY += 1
                        player.to_the_bottom()
                    elif event.key == pygame.K_w:
                        keyCountY += 1
                        player.to_the_top()
                    elif event.key == pygame.K_p:
                        game_state = PAUSED
                    elif event.key == pygame.K_SPACE:
                        # 雙發子彈攻擊
                        m_y = player._y
                        Missiles.append(MyMissile(xy=(player._x + 20, m_y), playground=playground, sensitivity=movingScale))
                        Missiles.append(MyMissile(xy=(player._x + 80, m_y), playground=playground, sensitivity=movingScale))
                        pygame.time.set_timer(launchMissile, 400)

                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_a, pygame.K_d]:
                        keyCountX = max(0, keyCountX - 1)
                        if keyCountX == 0:
                            player.stop_x()
                    elif event.key in [pygame.K_s, pygame.K_w]:
                        keyCountY = max(0, keyCountY - 1)
                        if keyCountY == 0:
                            player.stop_y()
                    elif event.key == pygame.K_SPACE:
                        pygame.time.set_timer(launchMissile, 0)

                elif event.type == launchMissile:
                    # 自動發射子彈
                    m_y = player._y
                    Missiles.append(MyMissile(xy=(player._x + 20, m_y), playground=playground, sensitivity=movingScale))
                    Missiles.append(MyMissile(xy=(player._x + 80, m_y), playground=playground, sensitivity=movingScale))

                elif event.type == createEnemy:
                    # 敵人與其子彈生成
                    e = Enemy(playground=playground, sensitivity=movingScale)
                    Enemies.append(e)
                    if random.random() < 0.5:
                        EnemyBullets.append(e.fire())

            # 暫停狀態
            elif game_state == PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_state = PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            # 結束狀態（Game Over）
            elif game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_state = MENU
                    elif event.key == pygame.K_ESCAPE:
                        running = False

        # 畫面更新：依遊戲狀態呈現內容（主選單、遊戲中、結束）
        if game_state == MENU:
            screen.blit(cover_bg, (0, 0))
            base_x = screenWidth // 2
            base_y = screenHigh // 2 - 100
            title_text = "射擊遊戲"

            # 加上文字描邊效果
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                outline = title_font.render(title_text, True, (255, 255, 255))
                rect = outline.get_rect(center=(base_x + dx, base_y + dy))
                screen.blit(outline, rect)

            main_title = title_font.render(title_text, True, (0, 0, 0))
            main_rect = main_title.get_rect(center=(base_x, base_y))
            screen.blit(main_title, main_rect)

            tip1 = font.render("[SPACE] Start", True, (255, 255, 255))
            tip2 = font.render("[ESC] Exit", True, (255, 255, 255))
            screen.blit(tip1, tip1.get_rect(center=(base_x, base_y + 130)))
            screen.blit(tip2, tip2.get_rect(center=(base_x, base_y + 200)))
            pygame.display.update()

        elif game_state == PLAYING:
            # 遊戲進行畫面
            screen.blit(background, (0, 0))

            # 檢查玩家是否碰撞到敵人或敵人子彈
            for e in Enemies:
                if player._collided_(e):
                    e.available = False
                    Boom.append(Explosion(e.center))
                    player._hp -= 10
                    explosion1.play()

            for b in EnemyBullets:
                if player._collided_(b):
                    b.available = False
                    player._hp -= 10
                    explosion1.play()

            # 檢查碰撞與分數更新
            player.collision_detect(Enemies)
            for m in Missiles:
                m.collision_detect(Enemies)
            for e in Enemies:
                if e.collided:
                    Boom.append(Explosion(e.center))
                    score += 10
                    explosion1.play()

            # 更新並顯示所有遊戲物件
            Missiles = [m for m in Missiles if m.available]
            for m in Missiles:
                m.update()
                screen.blit(m.image, m.xy)

            Enemies = [e for e in Enemies if e.available]
            for e in Enemies:
                e.update()
                screen.blit(e.image, e.xy)

            EnemyBullets = [b for b in EnemyBullets if b.available]
            for b in EnemyBullets:
                b.update()
                screen.blit(b.image, b.xy)

            Boom = [b for b in Boom if b.available]
            for b in Boom:
                b.update()
                screen.blit(b.image, b.xy)

            player.update()
            screen.blit(player.image, player.xy)

            # 血條顯示
            screen.blit(hp_font.render("HP", True, (255, 255, 255)), (20, 30))
            bar_x, bar_y, bar_w, bar_h = 70, 35, 200, 12
            pygame.draw.rect(screen, (0, 0, 0), (bar_x - 2, bar_y - 2, bar_w + 4, bar_h + 4))
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, max(0, player._hp / 100 * bar_w), bar_h))

            # 分數顯示
            score_text = font.render(f'Score: {score}', True, (255, 255, 0))
            score_rect = score_text.get_rect(topright=(screenWidth - 20, 10))
            screen.blit(score_text, score_rect)

            pygame.display.update()

            # 判斷是否遊戲結束
            if player._hp <= 0:
                high_score = max(high_score, score)
                game_state = GAME_OVER

        elif game_state == GAME_OVER:
            # 結束畫面顯示
            screen.fill((0, 0, 0))
            game_over_text = title_font.render('Game Over', True, (255, 0, 0))
            score_text = font.render(f'Score: {high_score}', True, (255, 255, 0))
            reset_text = font.render('[R] Reset', True, (255, 255, 255))

            screen.blit(game_over_text, game_over_text.get_rect(center=(screenWidth // 2, 190)))
            screen.blit(score_text, score_text.get_rect(center=(screenWidth // 2, 350)))
            screen.blit(reset_text, reset_text.get_rect(center=(screenWidth // 2, 400)))
            pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
