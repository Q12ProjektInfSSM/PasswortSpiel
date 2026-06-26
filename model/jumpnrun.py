import pygame
import random
import string


class JumpnRunGame:

    def __init__(self):
        self.code = "A7X9"

    def generate_captcha(self):
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def start(self):
        pygame.init()

        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Jump'n'Run Password Challenge")

        clock = pygame.time.Clock()
        running = True

        player = pygame.Rect(100, 450, 40, 40)

        vel_y = 0
        gravity = 0.6
        speed = 5
        on_ground = True

        # 🧱 echter Boden + Plattformen
        platforms = [
            pygame.Rect(0, 580, 800, 20),   # Boden
            pygame.Rect(200, 520, 80, 20),
            pygame.Rect(320, 480, 70, 20),
            pygame.Rect(450, 540, 90, 20),
            pygame.Rect(580, 500, 70, 20),
            pygame.Rect(700, 460, 60, 20),
        ]

        captcha = None
        game_won = False

        while running:
            clock.tick(60)
            screen.fill((135, 206, 235))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            # ➡️ Bewegung
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.x -= speed

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.x += speed

            # 🧱 Jump
            if keys[pygame.K_SPACE] and on_ground:
                vel_y = -12
                on_ground = False

            # 🌍 Gravity
            vel_y += gravity
            player.y += vel_y

            on_ground = False

            # 🧱 Plattform-Kollision
            for p in platforms:
                pygame.draw.rect(screen, (0, 0, 0), p)

                if player.colliderect(p):

                    # nur wenn FALLEN → landen
                    if vel_y > 0 and player.bottom - vel_y <= p.top:
                        player.bottom = p.top
                        vel_y = 0
                        on_ground = True

                    # von unten
                    elif vel_y < 0 and player.top < p.bottom:
                        player.top = p.bottom
                        vel_y = 0

            # 👤 Spieler
            pygame.draw.rect(screen, (255, 0, 0), player)

            # 🎯 Ziel
            if player.x > 760 and not game_won:
                game_won = True
                captcha = self.generate_captcha()

            # 🔐 CAPTCHA
            if game_won:
                font = pygame.font.SysFont(None, 60)
                text = font.render(f"CAPTCHA: {captcha}", True, (0, 0, 0))
                screen.blit(text, (200, 250))

            pygame.display.flip()

        pygame.quit()

        return self.code, captcha


