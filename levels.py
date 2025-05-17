import pygame
import sys
from pygame import mixer
from typing import Tuple, Dict
import math
from PIL import Image  # For loading GIF frames

# Initialize Pygame
pygame.init()
mixer.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 81, 255)
YELLOW = (255, 204, 0)
GREEN = (0, 255, 0)
PURPLE = (147, 0, 211)

# Initialize window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ultimate Boxing Championship II - Level 1")
clock = pygame.time.Clock()

# Load fonts
try:
    game_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 24)
    timer_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 48)
except:
    game_font = pygame.font.SysFont("Arial", 24)
    timer_font = pygame.font.SysFont("Arial", 48)

# Function to load and resize GIF frames
def load_gif_frames(gif_path: str, size: Tuple[int, int]) -> list:
    frames = []
    try:
        pil_image = Image.open(gif_path)
        for frame in range(pil_image.n_frames):
            pil_image.seek(frame)
            frame_image = pil_image.convert("RGB").resize(size)
            mode = frame_image.mode
            data = frame_image.tobytes()
            surface = pygame.image.fromstring(data, frame_image.size, mode)
            frames.append(surface)
    except Exception as e:
        print(f"Error loading GIF: {e}")
    return frames

class Fighter:
    def __init__(self, name: str, color: Tuple[int, int, int], position: Tuple[int, int]):
        self.name = name
        self.color = color
        self.position = position
        self.health = 100
        self.aura = 100
        self.rounds_won = 0
        self.is_blocking = False
        self.aura_charging = False
        self.aura_effect_timer = 0

    def draw(self):
        fighter_rect = pygame.Rect(self.position[0], self.position[1], 100, 200)
        pygame.draw.rect(screen, self.color, fighter_rect)

        if self.aura_charging:
            self.aura_effect_timer = (self.aura_effect_timer + 1) % 360
            for i in range(0, 360, 30):
                angle = math.radians(i + self.aura_effect_timer)
                radius = 60
                x = self.position[0] + 50 + radius * math.cos(angle)
                y = self.position[1] + 100 + radius * math.sin(angle)
                pygame.draw.circle(screen, PURPLE, (int(x), int(y)), 5)

class Level:
    def __init__(self, player_character: Dict):
        self.round_time = 99
        self.current_time = self.round_time
        self.timer_active = True

        self.player = Fighter(player_character["name"], player_character["color"], (200, 400))
        self.opponent = Fighter("CPU", RED, (900, 400))

        # Load animated GIF background
        self.bg_frames = load_gif_frames("assets/background/underground.gif", (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.current_frame = 0
        self.frame_timer = 0

        try:
            mixer.music.load("assets/music/fight_theme.mp3")
            mixer.music.play(-1)
        except:
            print("Background music could not be loaded")

    def draw_health_bars(self):
        pygame.draw.rect(screen, RED, (50, 50, 400, 30))
        pygame.draw.rect(screen, GREEN, (50, 50, self.player.health * 4, 30))
        pygame.draw.rect(screen, WHITE, (50, 50, 400, 30), 3)

        pygame.draw.rect(screen, RED, (750, 50, 400, 30))
        pygame.draw.rect(screen, GREEN, (750, 50, self.opponent.health * 4, 30))
        pygame.draw.rect(screen, WHITE, (750, 50, 400, 30), 3)

    def draw_aura_bars(self):
        pygame.draw.rect(screen, BLUE, (50, 90, 400, 20))
        pygame.draw.rect(screen, YELLOW, (50, 90, self.player.aura * 4, 20))
        pygame.draw.rect(screen, WHITE, (50, 90, 400, 20), 2)

        pygame.draw.rect(screen, BLUE, (750, 90, 400, 20))
        pygame.draw.rect(screen, YELLOW, (750, 90, self.opponent.aura * 4, 20))
        pygame.draw.rect(screen, WHITE, (750, 90, 400, 20), 2)

    def draw_timer(self):
        timer_text = timer_font.render(str(max(0, int(self.current_time))), True, WHITE)
        timer_rect = timer_text.get_rect(center=(WINDOW_WIDTH // 2, 60))
        screen.blit(timer_text, timer_rect)

    def draw_round_wins(self):
        for i in range(self.player.rounds_won):
            pygame.draw.circle(screen, YELLOW, (50 + i * 30, 130), 10)
        for i in range(self.opponent.rounds_won):
            pygame.draw.circle(screen, YELLOW, (1150 - i * 30, 130), 10)

    def update_background(self):
        if self.bg_frames:
            self.frame_timer += 1
            if self.frame_timer >= 10:  # Adjust speed
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.bg_frames)
            screen.blit(self.bg_frames[self.current_frame], (0, 0))
        else:
            screen.fill((0, 0, 0))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.player.is_blocking = True
                    elif event.key == pygame.K_LSHIFT:
                        self.player.aura_charging = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.player.is_blocking = False
                    elif event.key == pygame.K_LSHIFT:
                        self.player.aura_charging = False

            if self.timer_active and self.current_time > 0:
                self.current_time -= 1 / FPS

            self.update_background()
            self.player.draw()
            self.opponent.draw()
            self.draw_health_bars()
            self.draw_aura_bars()
            self.draw_timer()
            self.draw_round_wins()

            pygame.display.flip()
            clock.tick(FPS)

def start_level_one(player_character):
    level = Level(player_character)
    return level.run()

if __name__ == "__main__":
    test_character = {
        "name": "CRUSHER",
        "color": BLUE,
        "stats": {
            "POWER": 9,
            "SPEED": 5,
            "STAMINA": 7,
            "TECHNIQUE": 6
        }
    }
    start_level_one(test_character)
