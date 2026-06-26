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

        WORLD_WIDTH = 4000

        # 🧍 Respawn Position
        spawn_x = 100
        spawn_y = 450

        player = pygame.Rect(spawn_x, spawn_y, 40, 40)

        vel_y = 0
        gravity = 0.6
        speed = 5
        on_ground = True

        # 🧱 Plattformen (ENGER + SPIELBARER)
        platforms = []

        # Boden
        platforms.append(pygame.Rect(0, 580, WORLD_WIDTH, 20))

        # 🧠 bessere Verteilung: näher & gleichmäßiger
        x = 200
        while x < WORLD_WIDTH - 200:
            y = random.choice([520, 500, 480, 460, 520])
            platforms.append(pygame.Rect(x, y, 120, 20))
            x += random.randint(180, 260)

        captcha = None
        game_won = False

        camera_x = 0

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

            # 🧱 Kollision
            for p in platforms:
                if player.colliderect(p):

                    # von oben landen
                    if vel_y > 0 and player.bottom - vel_y <= p.top:
                        player.bottom = p.top
                        vel_y = 0
                        on_ground = True

                    # von unten blockieren
                    elif vel_y < 0:
                        player.top = p.bottom
                        vel_y = 0

            # 💀 FALL-DEAD ZONE → Respawn
            if player.y > 650:
                player.x = spawn_x
                player.y = spawn_y
                vel_y = 0

            # 🎥 Kamera
            camera_x = player.x - 300
            camera_x = max(0, min(camera_x, WORLD_WIDTH - 800))

            # 🧱 Zeichnen Plattformen
            for p in platforms:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(
                    p.x - camera_x,
                    p.y,
                    p.width,
                    p.height
                ))

            # 👤 Spieler
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(
                player.x - camera_x,
                player.y,
                player.width,
                player.height
            ))

            # 🎯 Ziel
            if player.x > WORLD_WIDTH - 150 and not game_won:
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


if __name__ == "__main__":
    game = JumpnRunGame()
    print(game.start())