import pygame
import random
from pathlib import Path
from player import Player
from missle import MyMissile
from enemy import Enemy
from explosion import Explosion
from enemy_bullet import EnemyBullet
from gobject import GameObject

def main():
    # 資料夾路徑與資源路徑設定
    parent_path = Path(__file__).parents[1]
    image_path = parent_path / 'res'
    icon_path = image_path / 'airplaneicon.png'
    font_path = str(image_path / 'msjh.ttc')
    bg_path = image_path / 'background.png'
    cover_path = image_path / 'cover_image.png'

    pygame.init()
    pygame.mixer.init()

    # 畫面尺寸設定與爆炸音效載入
    screenHigh = 800
    screenWidth = 1200
    playground = [screenWidth, screenHigh]
    explosion1 = pygame.mixer.Sound(str(image_path / 'explosion1.mp3'))

    screen = pygame.display.set_mode((screenWidth, screenHigh))
    pygame.display.set_caption("射擊遊戲")
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    # 背景與封面圖
    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (screenWidth, screenHigh))

    cover_bg = pygame.image.load(cover_path).convert()
    cover_bg = pygame.transform.scale(cover_bg, (screenWidth, screenHigh))

    # 字型設定
    font = pygame.font.Font(font_path, 40)
    title_font = pygame.font.SysFont("Microsoft JhengHei", 80, bold=True)
    hp_font = pygame.font.SysFont("Microsoft JhengHei", 24, bold=True)

    fps = 120
    clock = pygame.time.Clock()
    movingScale = 1000 / fps

    # 遊戲對象與狀態變數
    player = Player(playground=playground, sensitivity=movingScale)
    player._hp = 100
    keyCountX = 0
    keyCountY = 0
    Missiles = []
    Enemies = []
    Boom = []
    EnemyBullets = []

    # 發射與產生敵人
    launchMissile = pygame.USEREVENT + 1
    createEnemy = pygame.USEREVENT + 2
    pygame.time.set_timer(createEnemy, 400)  # 敵人出現速度

    score = 0
    high_score = 0

    # 遊戲狀態定義
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    game_state = MENU

    running = True

    while running:
        dt = clock.tick(fps)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #  主選單
            if game_state == MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
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
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # 遊戲進行中
            elif game_state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        keyCountX += 1
                        player.to_the_left()
                    if event.key == pygame.K_d:
                        keyCountX += 1
                        player.to_the_right()
                    if event.key == pygame.K_s:
                        keyCountY += 1
                        player.to_the_bottom()
                    if event.key == pygame.K_w:
                        keyCountY += 1
                        player.to_the_top()
                    if event.key == pygame.K_p:
                        game_state = PAUSED
                    if event.key == pygame.K_SPACE:
                        m_x = player._x + 20  # 子彈向左移
                        m_y = player._y
                        Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                        m_x = player._x + 80
                        Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                        pygame.time.set_timer(launchMissile, 400)

                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_a, pygame.K_d]:
                        keyCountX = max(0, keyCountX - 1)
                        if keyCountX == 0:
                            player.stop_x()
                    if event.key in [pygame.K_s, pygame.K_w]:
                        keyCountY = max(0, keyCountY - 1)
                        if keyCountY == 0:
                            player.stop_y()
                    if event.key == pygame.K_SPACE:
                        pygame.time.set_timer(launchMissile, 0)

                if event.type == launchMissile:
                    m_x = player._x + 20
                    m_y = player._y
                    Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                    m_x = player._x + 80
                    Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))

                if event.type == createEnemy:
                    e = Enemy(playground=playground, sensitivity=movingScale)
                    Enemies.append(e)
                    if random.random() < 0.5:
                        EnemyBullets.append(e.fire())

            # 遊戲暫停
            elif game_state == PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_state = PLAYING
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # 遊戲結束
            elif game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_state = MENU
                    if event.key == pygame.K_ESCAPE:
                        running = False

        # 遊戲主邏輯與繪製
        if game_state == MENU:
            screen.blit(cover_bg, (0, 0))
            base_x = screenWidth // 2
            base_y = screenHigh // 2 - 100
            if game_state == MENU:
                screen.blit(cover_bg, (0, 0))
                base_x = screenWidth // 2
                base_y = screenHigh // 2 - 100
                title_text = "射擊遊戲"

                # 白邊描邊效果
                for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                    outline = title_font.render(title_text, True, (255, 255, 255))
                    rect = outline.get_rect(center=(base_x + dx, base_y + dy))
                    screen.blit(outline, rect)

                # 黑色主標題文字
                main_title = title_font.render(title_text, True, (0, 0, 0))
                main_rect = main_title.get_rect(center=(base_x, base_y))
                screen.blit(main_title, main_rect)

                screen.blit(font.render("[SPACE] Start", True, (255, 255, 255)), (base_x - 100, base_y + 80))
                screen.blit(font.render("[ESC] Exit", True, (255, 255, 255)), (base_x - 100, base_y + 140))
                pygame.display.update()

        elif game_state == PLAYING:
            screen.blit(background, (0, 0))

            # 玩家碰撞處理
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

            player.collision_detect(Enemies)
            for m in Missiles:
                m.collision_detect(Enemies)

            for e in Enemies:
                if e.collided:
                    Boom.append(Explosion(e.center))
                    score += 10
                    explosion1.play()

            # 更新所有對象
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

            # 血條 + 分數顯示
            screen.blit(hp_font.render("HP", True, (255, 255, 255)), (20, 30))
            bar_x, bar_y, bar_w, bar_h = 70, 35, 200, 12
            pygame.draw.rect(screen, (0, 0, 0), (bar_x - 2, bar_y - 2, bar_w + 4, bar_h + 4))
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, max(0, player._hp / 100 * bar_w), bar_h))

            score_text = font.render(f'Score: {score}', True, (255, 255, 0))
            score_rect = score_text.get_rect(topright=(screenWidth - 20, 10))
            screen.blit(score_text, score_rect)

            pygame.display.update()

            if player._hp <= 0:
                high_score = max(high_score, score)
                game_state = GAME_OVER

        elif game_state == GAME_OVER:
            screen.fill((0, 0, 0))
            screen.blit(title_font.render('Game Over', True, (255, 0, 0)), (screenWidth//2 - 200, 250))
            screen.blit(font.render(f'Score: {high_score}', True, (255, 255, 0)), (screenWidth//2 - 100, 400))
            screen.blit(font.render('[R] Reset', True, (255, 255, 255)), (screenWidth//2 - 100, 480))
            pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
