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
    hp_font = pygame.font.Font(font_path, 28)
    game_over_font = pygame.font.Font(font_path, 80)  # ✅ Game Over 粗大字體
    title_font = pygame.font.SysFont("Microsoft JhengHei", 80, bold=True)

    fps = 120
    clock = pygame.time.Clock()
    movingScale = 1000 / fps

    player = Player(playground=playground, sensitivity=movingScale)
    player._hp = 100
    keyCountX = 0
    keyCountY = 0
    Missiles = []
    Enemies = []
    Boom = []
    EnemyBullets = []

    launchMissile = pygame.USEREVENT + 1
    createEnemy = pygame.USEREVENT + 2
    pygame.time.set_timer(createEnemy, 600)

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
                if e.collided and not player._collided_(e):
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
            hp_label = hp_font.render("HP", True, (255, 255, 255))
            screen.blit(hp_label, (20, 20))

            max_bar_width = 200
            bar_height = 12
            bar_x, bar_y = 70, 35
            pygame.draw.rect(screen, (0, 0, 0), (bar_x - 2, bar_y - 2, max_bar_width + 4, bar_height + 4))
            pygame.draw.rect(screen, (0, 100, 0), (bar_x, bar_y, max_bar_width, bar_height))
            current_bar_width = max(0, player._hp / 100 * max_bar_width)
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, current_bar_width, bar_height))

            score_text = font.render(f'Score: {score}', True, (255, 255, 0))
            score_rect = score_text.get_rect(topright=(screenWidth - 20, 10))
            screen.blit(score_text, score_rect)

            pygame.display.update()

            if player._hp <= 0:
                high_score = max(high_score, score)
                game_state = GAME_OVER

        elif game_state == GAME_OVER:
            screen.fill((0, 0, 0))

            # ✅ Game Over 加大置中
            game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(screenWidth // 2, 250))
            screen.blit(game_over_text, game_over_rect)

            score_text = font.render(f'Score: {high_score}', True, (255, 255, 0))
            score_rect = score_text.get_rect(center=(screenWidth // 2, 400))
            screen.blit(score_text, score_rect)

            reset_text = font.render('[R]Reset', True, (255, 255, 255))
            reset_rect = reset_text.get_rect(center=(screenWidth // 2, 500))
            screen.blit(reset_text, reset_rect)

            pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
