import pygame
import sys
from pygame import mixer
from typing import Tuple, Dict
import math
from PIL import Image

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
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ultimate Boxing Championship II")
clock = pygame.time.Clock()

# Fonts
try:
    game_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 24)
    timer_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 48)
except:
    game_font = pygame.font.SysFont("Arial", 24)
    timer_font = pygame.font.SysFont("Arial", 48)

# Load music
try:
    mixer.music.load("assets/music/fight_theme.mp3")
    mixer.music.play(-1)
except:
    print("Music file could not be loaded.")

# Function to load and resize GIF frames
def load_gif_frames(path: str, size: Tuple[int, int]) -> list:
    frames = []
    try:
        img = Image.open(path)
        for frame in range(img.n_frames):
            img.seek(frame)
            frame_img = img.convert("RGB").resize(size)

            mode = frame_img.mode
            data = frame_img.tobytes()
            surface = pygame.image.fromstring(data, frame_img.size, mode)  # use resized size here
            frames.append(surface)
    except Exception as e:
        print(f"Error loading GIF frames from: {path}\n{e}")
    return frames


class Fighter:
    def __init__(self, name, color, position):
        self.name = name
        self.color = color
        self.position = position
        self.health = 100
        self.aura = 100
        self.rounds_won = 0
        self.is_blocking = False
        self.aura_charging = False
        self.aura_timer = 0

    def draw(self):
        fighter_rect = pygame.Rect(self.position[0], self.position[1], 100, 200)
        pygame.draw.rect(screen, self.color, fighter_rect)
        if self.aura_charging:
            self.aura_timer = (self.aura_timer + 1) % 360
            for i in range(0, 360, 30):
                angle = math.radians(i + self.aura_timer)
                x = self.position[0] + 50 + 60 * math.cos(angle)
                y = self.position[1] + 100 + 60 * math.sin(angle)
                pygame.draw.circle(screen, PURPLE, (int(x), int(y)), 5)

class Level:
    def __init__(self, player, opponent_name, opponent_color, bg_path=None):
        self.round_time = 5
        self.current_time = self.round_time
        self.timer_active = True

        self.player = Fighter(player["name"], player["color"], (200, 400))
        self.opponent = Fighter(opponent_name, opponent_color, (900, 400))

        # Background
        self.bg_frames = load_gif_frames(bg_path, (WINDOW_WIDTH, WINDOW_HEIGHT)) if bg_path else []
        self.bg_index = 0
        self.bg_timer = 0

    def draw_background(self):
        if self.bg_frames:
            self.bg_timer += 1
            if self.bg_timer >= 10:
                self.bg_timer = 0
                self.bg_index = (self.bg_index + 1) % len(self.bg_frames)
            screen.blit(self.bg_frames[self.bg_index], (0, 0))
        else:
            screen.fill(BLACK)  # Placeholder if background is missing

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

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.player.is_blocking = True
                    elif event.key == pygame.K_LSHIFT:
                        self.player.aura_charging = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.player.is_blocking = False
                    elif event.key == pygame.K_LSHIFT:
                        self.player.aura_charging = False

            if self.timer_active and self.current_time > 0:
                self.current_time -= 1 / FPS

            self.draw_background()
            self.player.draw()
            self.opponent.draw()
            self.draw_health_bars()
            self.draw_aura_bars()
            self.draw_timer()
            self.draw_round_wins()

                        # Check if time ran out
            if self.current_time <= 0:
                self.timer_active = False
                win_text = game_font.render("You win! Press ENTER to continue...", True, WHITE)
                screen.blit(win_text, (WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2))
                pygame.display.flip()

                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit(); sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                return True
                            elif event.key == pygame.K_ESCAPE:
                                pygame.quit(); sys.exit()
                    clock.tick(FPS)

            pygame.display.flip()
            clock.tick(FPS)

        return True


def play_cutscene():
    screen.fill(BLACK)
    text_lines = [
        "After defeating your first opponent...",
        "You prepare for the ultimate showdown.",
        "Next Opponent: SHADOW VIPER.",
        "Press ENTER to continue or ESC to quit."
    ]
    for i, line in enumerate(text_lines):
        text = game_font.render(line, True, WHITE)
        screen.blit(text, (100, 250 + i * 40))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False

def main_game():
    player_data = {
        "name": "CRUSHER",
        "color": BLUE
    }

    # Level 1
    level1 = Level(player_data, "CPU", RED, bg_path="assets/background/underground.gif")
    level1.run()

    # Cutscene & transition
    if play_cutscene():
        # Level 2 with placeholder background
        level2 = Level(player_data, "SHADOW VIPER", PURPLE, bg_path=None)  # Placeholder
        level2.run()
    else:
        print("Player chose not to continue.")

if __name__ == "__main__":
    main_game()
