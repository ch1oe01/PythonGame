import pygame
import random
from pathlib import Path
from player import Player
from missle import MyMissile
from enemy import Enemy
from explosion import Explosion
from enemy_bullet import EnemyBullet  # 加入敵人子彈
from gobject import GameObject

def main():
    parent_path = Path(__file__).parents[1]
    image_path = parent_path / 'res'
    icon_path = image_path / 'airplaneicon.png'
    font_path = str(image_path / 'msjh.ttc')
    bg_path = image_path / 'background.png'
    cover_path = image_path / 'cover_image.png'

    pygame.init()
    pygame.mixer.init()

    screenHigh = 800
    screenWidth = 1200
    playground = [screenWidth, screenHigh]
    explosion_sound = pygame.mixer.Sound(str(image_path / 'explosion.mp3'))

    screen = pygame.display.set_mode((screenWidth, screenHigh))
    pygame.display.set_caption("射擊遊戲")
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, (screenWidth, screenHigh))

    cover_bg = pygame.image.load(cover_path).convert()
    cover_bg = pygame.transform.scale(cover_bg, (screenWidth, screenHigh))

    font = pygame.font.Font(font_path, 40)
    title_font = pygame.font.SysFont("Microsoft JhengHei", 80, bold=True)

    game_duration = 30
    fps = 120
    clock = pygame.time.Clock()
    movingScale = 1000 / fps

    player = Player(playground=playground, sensitivity=movingScale)
    player._hp = 100  # 初始血量
    keyCountX = 0
    keyCountY = 0
    Missiles = []
    Enemies = []
    Boom = []
    EnemyBullets = []

    launchMissile = pygame.USEREVENT + 1
    createEnemy = pygame.USEREVENT + 2
    pygame.time.set_timer(createEnemy, 1000)

    score = 0
    high_score = 0
    start_ticks = None

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

            if game_state == MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = PLAYING
                        start_ticks = pygame.time.get_ticks()
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
                        m_x = player._x + 40
                        m_y = player._y
                        Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                        m_x = player._x + 100
                        Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                        pygame.time.set_timer(launchMissile, 400)

                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_a, pygame.K_d]:
                        if keyCountX == 1:
                            keyCountX = 0
                            player.stop_x()
                        else:
                            keyCountX -= 1
                    if event.key in [pygame.K_s, pygame.K_w]:
                        if keyCountY == 1:
                            keyCountY = 0
                            player.stop_y()
                        else:
                            keyCountY -= 1
                    if event.key == pygame.K_SPACE:
                        pygame.time.set_timer(launchMissile, 0)

                if event.type == launchMissile:
                    m_x = player._x + 40
                    m_y = player._y
                    Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                    m_x = player._x + 100
                    Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))

                if event.type == createEnemy:
                    e = Enemy(playground=playground, sensitivity=movingScale)
                    Enemies.append(e)
                    if random.random() < 0.5:
                        EnemyBullets.append(e.fire())

            elif game_state == PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_state = PLAYING
                    if event.key == pygame.K_ESCAPE:
                        running = False

            elif game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_state = MENU
                    if event.key == pygame.K_ESCAPE:
                        running = False

        if game_state == MENU:
            screen.blit(cover_bg, (0, 0))
            title_text = "射擊遊戲"
            base_x = screenWidth // 2
            base_y = screenHigh // 2 - 100

            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                outline = title_font.render(title_text, True, (255, 255, 255))
                rect = outline.get_rect(center=(base_x + dx, base_y + dy))
                screen.blit(outline, rect)

            main_title = title_font.render(title_text, True, (0, 0, 0))
            main_rect = main_title.get_rect(center=(base_x, base_y))
            screen.blit(main_title, main_rect)

            screen.blit(font.render("[SPACE] Start", True, (255, 255, 255)), (base_x - 100, base_y + 80))
            screen.blit(font.render("[ESC] Exit", True, (255, 255, 255)), (base_x - 100, base_y + 140))
            pygame.display.update()

        elif game_state == PLAYING:
            screen.blit(background, (0, 0))

            # 碰撞處理
            for e in Enemies:
                if player._collided_(e):
                    e.available = False
                    Boom.append(Explosion(e.center))
                    player._hp -= 10

            for b in EnemyBullets:
                if player._collided_(b):
                    b.available = False
                    player._hp -= 10

            player.collision_detect(Enemies)
            for m in Missiles:
                m.collision_detect(Enemies)

            for e in Enemies:
                if e.collided:
                    Boom.append(Explosion(e.center))
                    score += 10
                    explosion_sound.play()

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

            # 血條
            max_bar_width = 200
            bar_x, bar_y = 10, 10
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, max_bar_width, 25))
            current_bar_width = max(0, player._hp / 100 * max_bar_width)
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, current_bar_width, 25))

            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            remaining_time = max(0, game_duration - int(seconds))
            countdown = font.render(f'Time: {remaining_time}', True, (255, 255, 255))
            score_text = font.render(f'Score: {score}', True, (255, 255, 0))
            screen.blit(countdown, (10, 45))
            screen.blit(score_text, (10, 80))

            pygame.display.update()

            if player._hp <= 0:
                high_score = max(high_score, score)
                game_state = GAME_OVER

        elif game_state == PAUSED:
            pause_text = font.render("遊戲暫停", True, (255, 255, 0))
            continue_text = font.render("[P] 繼續遊戲", True, (255, 255, 255))
            screen.blit(pause_text, (screenWidth // 2 - 80, screenHigh // 2 - 40))
            screen.blit(continue_text, (screenWidth // 2 - 100, screenHigh // 2 + 20))
            pygame.display.update()

        elif game_state == GAME_OVER:
            screen.fill((0, 0, 0))
            screen.blit(font.render('Game Over', True, (255, 0, 0)), (screenWidth//2 - 100, 200))
            screen.blit(font.render(f'Score: {high_score}', True, (255, 255, 0)), (screenWidth//2 - 100, 300))
            screen.blit(font.render('[R]Reset', True, (255, 255, 255)), (screenWidth//2 - 100, 400))
            pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
