import pygame
from pathlib import Path
from player import Player
from missle import MyMissile
from enemy import Enemy
from explosion import Explosion
from gobject import GameObject

def main():
    parent_path = Path(__file__).parents[1]
    image_path = parent_path / 'res'
    icon_path = image_path / 'airplaneicon.png'
    font_path  = str(image_path / 'msjh.ttc')  # 中文字型

    pygame.init()
    pygame.mixer.init()

    screenHigh = 600
    screenWidth = 1200
    playground = [screenWidth, screenHigh]
    explosion_sound = pygame.mixer.Sound(str(image_path / 'explosion.mp3'))

    screen = pygame.display.set_mode((screenWidth, screenHigh))
    pygame.display.set_caption("射擊遊戲")
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((50, 50, 50))

    game_duration = 30  # 秒
    font = pygame.font.Font(font_path, 40)  # 使用中文字型

    fps = 120
    clock = pygame.time.Clock()
    movingScale = 1000 / fps

    player = Player(playground=playground, sensitivity=movingScale)
    keyCountX = 0
    keyCountY = 0
    Missiles = []
    Enemies = []
    Boom = []

    launchMissile = pygame.USEREVENT + 1
    createEnemy = pygame.USEREVENT + 2
    pygame.time.set_timer(createEnemy, 1000)

    score = 0
    high_score = 0
    start_ticks = None

    MENU = "menu"
    PLAYING = "playing"
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
                        score = 0
                        player = Player(playground=playground, sensitivity=movingScale)
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
                    if event.key == pygame.K_SPACE:
                        m_x = player._x + 20
                        m_y = player._y
                        Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                        m_x = player._x + 80
                        Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                        pygame.time.set_timer(launchMissile, 400)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        if keyCountX == 1:
                            keyCountX = 0
                            player.stop_x()
                        else:
                            keyCountX -= 1
                    if event.key == pygame.K_s or event.key == pygame.K_w:
                        if keyCountY == 1:
                            keyCountY = 0
                            player.stop_y()
                        else:
                            keyCountY -= 1
                    if event.key == pygame.K_SPACE:
                        pygame.time.set_timer(launchMissile, 0)

                if event.type == launchMissile:
                    m_x = player._x + 20
                    m_y = player._y
                    Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                    m_x = player._x + 80
                    Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))

                if event.type == createEnemy:
                    Enemies.append(Enemy(playground=playground, sensitivity=movingScale))

            elif game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_state = MENU
                    if event.key == pygame.K_ESCAPE:
                        running = False

        if game_state == MENU:
            title = font.render("射擊遊戲", True, (255, 0, 0))
            start = font.render("[SPACE] Start", True, (255, 255, 255))
            quit_text = font.render("[ESC] Exit", True, (255, 255, 255))
            screen.blit(title, (screenWidth//2 - title.get_width()//2, 200))
            screen.blit(start, (screenWidth//2 - start.get_width()//2, 300))
            screen.blit(quit_text, (screenWidth//2 - quit_text.get_width()//2, 400))
            pygame.display.update()

        elif game_state == PLAYING:
            screen.blit(background, (0, 0))

            player.collision_detect(Enemies)
            for m in Missiles:
                m.collision_detect(Enemies)

            for e in Enemies:
                if e.collided:
                    Boom.append(Explosion(e.center))
                    score += 10  # 擊落加分
                    explosion_sound.play()

            Missiles = [m for m in Missiles if m.available]
            for m in Missiles:
                m.update()
                screen.blit(m.image, m.xy)

            Enemies = [e for e in Enemies if e.available]
            for e in Enemies:
                e.update()
                screen.blit(e.image, e.xy)

            Boom = [b for b in Boom if b.available]
            for b in Boom:
                b.update()
                screen.blit(b.image, b.xy)

            player.update()
            screen.blit(player.image, player.xy)

            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            remaining_time = max(0, game_duration - int(seconds))

            countdown = font.render(f'Time: {remaining_time}', True, (255, 255, 255))
            score_text = font.render(f'Score: {score}', True, (255, 255, 0))
            screen.blit(countdown, (10, 10))
            screen.blit(score_text, (10, 70))

            pygame.display.update()

            if remaining_time == 0:
                if score > high_score:
                    high_score = score
                game_state = GAME_OVER

        elif game_state == GAME_OVER:
            screen.fill((0, 0, 0))
            over_text = font.render('Game Over', True, (255, 0, 0))
            restart_text = font.render('[R]Reset', True, (255, 255, 255))
            best_score_text = font.render(f'Score: {high_score}', True, (255, 255, 0))

            screen.blit(over_text, (screenWidth//2 - over_text.get_width()//2, 200))
            screen.blit(best_score_text, (screenWidth//2 - best_score_text.get_width()//2, 300))
            screen.blit(restart_text, (screenWidth//2 - restart_text.get_width()//2, 400))
            pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
