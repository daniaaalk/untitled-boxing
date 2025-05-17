import pygame
import sys
import math
import game_state

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (234, 56, 76)
BLUE = (37, 99, 235)
YELLOW = (234, 179, 8)
GRAY = (100, 100, 100)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UNTITLED BOXING")
clock = pygame.time.Clock()

# Load fonts
try:
    title_font = pygame.font.Font("freesansbold.ttf", 60)
    menu_font = pygame.font.Font("freesansbold.ttf", 36)
    info_font = pygame.font.Font("freesansbold.ttf", 20)
except:
    title_font = pygame.font.SysFont("Arial", 60)
    menu_font = pygame.font.SysFont("Arial", 36)
    info_font = pygame.font.SysFont("Arial", 20)

# Placeholder assets
bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_img.fill((20, 20, 50))

# Sounds (optional)
try:
    select_sound = pygame.mixer.Sound("select.wav")
    hover_sound = pygame.mixer.Sound("hover.wav")
    pygame.mixer.music.load("menu_theme.mp3")
    pygame.mixer.music.set_volume(0.5)
    sound_loaded = True
except:
    sound_loaded = False
    print("Sound files could not be loaded. Continuing without sound.")

menu_items = ["START FIGHT", "OPTIONS", "EXIT"]
selected_item = 0
last_selected = 0
animation_counter = 0

# Characters
characters = [
    {
        "name": "Den \"Phantom\" Lai",
        "backstory": "Once a child of the streets of Neo Kowloon... vanished after a gang war.",
        "passive": ("Fade Step", 4),
        "special": ("Phase Strike", 5),
        "color": BLUE
    },
    {
        "name": "Kal \"Ghostline\" El",
        "backstory": "Ex-agent betrayed and rebuilt by tech rebels... now hunts his enemies.",
        "passive": ("Echo Reflex", 5),
        "special": ("Blackout Field", 4),
        "color": GRAY
    },
    {
        "name": "Kira \"Razorfang\" Aoyama",
        "backstory": "An experimental weapon from NeonGene Corp... seeks the truth of his past.",
        "passive": ("Neural Reflex Sync", 5),
        "special": ("Phantom Edge", 5),
        "color": RED
    }
]

current_character = 0
transition_alpha = 255
transitioning = False
transition_dir = 0

# Draw helper
star_img = pygame.Surface((20, 20))
pygame.draw.polygon(star_img, YELLOW, [(10, 0), (12, 7), (20, 7), (14, 12),
                                       (16, 20), (10, 15), (4, 20), (6, 12), (0, 7), (8, 7)])

def draw_text(text, font, color, x, y):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

def draw_stars(x, y, count):
    for i in range(count):
        screen.blit(star_img, (x + i * 25, y))

def draw_character_card(index):
    char = characters[index]

    screen.fill(BLACK)
    pygame.draw.rect(screen, char["color"], (50, 150, 200, 300))  # Portrait box
    pygame.draw.rect(screen, WHITE, (50, 150, 200, 300), 3)

    draw_text(char["name"], menu_font, YELLOW, 280, 150)
    draw_text("Backstory:", info_font, WHITE, 280, 200)
    draw_text(char["backstory"], info_font, GRAY, 280, 230)

    draw_text(f"Passive: {char['passive'][0]}", info_font, WHITE, 280, 280)
    draw_stars(280, 310, char['passive'][1])

    draw_text(f"Special: {char['special'][0]}", info_font, WHITE, 280, 360)
    draw_stars(280, 390, char['special'][1])

    draw_text("Press ENTER to select, ←/→ to switch, ESC to go back", info_font, GRAY, 200, 500)

def character_select_screen():
    global current_character, transitioning, transition_alpha, transition_dir
    selecting = True
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)

    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return game_state.EXIT
            if event.type == pygame.KEYDOWN:
                if not transitioning:
                    if event.key == pygame.K_ESCAPE:
                        return game_state.MENU
                    if event.key == pygame.K_RETURN:
                        print("Character selected! Starting game...")
                        return game_state.GAMEPLAY
                    if event.key == pygame.K_RIGHT:
                        current_character = (current_character + 1) % len(characters)
                        transitioning = True
                        transition_dir = -1
                        transition_alpha = 255
                    if event.key == pygame.K_LEFT:
                        current_character = (current_character - 1) % len(characters)
                        transitioning = True
                        transition_dir = 1
                        transition_alpha = 255

        draw_character_card(current_character)

        if transitioning:
            fade_surface.set_alpha(transition_alpha)
            screen.blit(fade_surface, (0, 0))
            transition_alpha -= 15
            if transition_alpha <= 0:
                transitioning = False

        pygame.display.flip()
        clock.tick(FPS)

def draw_menu():
    global animation_counter
    screen.blit(bg_img, (0, 0))

    y_offset = math.sin(animation_counter * 0.05) * 10
    pygame.draw.rect(screen, BLUE, (50, 250 + y_offset, 150, 300))
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH - 200, 250 - y_offset, 150, 300))

    pulse_value = (math.sin(animation_counter * 0.1) + 1) * 0.5
    glow_amount = int(3 + pulse_value * 5)
    draw_text("UNTITLED", title_font, RED, SCREEN_WIDTH // 2 - 100, 100)
    draw_text("BOXING", title_font, RED, SCREEN_WIDTH // 2 - 100, 170)

    for i, item in enumerate(menu_items):
        y_pos = 300 + i * 60
        color = YELLOW if i == selected_item else WHITE
        text_surf = menu_font.render(item, True, color)
        rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
        screen.blit(text_surf, rect)
        if i == selected_item:
            pygame.draw.rect(screen, RED, rect.inflate(30, 10), 2)

    draw_text("© 2025 G19 STUDIOS", pygame.font.SysFont("Arial", 16), WHITE, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT - 30)
    animation_counter += 1

def main_menu():
    global selected_item, last_selected
    if sound_loaded:
        pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return game_state.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                    if sound_loaded and last_selected != selected_item:
                        hover_sound.play()
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                    if sound_loaded and last_selected != selected_item:
                        hover_sound.play()
                elif event.key == pygame.K_RETURN:
                    if sound_loaded:
                        select_sound.play()
                    if selected_item == 0:
                        return game_state.CHARACTER_SELECT
                    elif selected_item == 1:
                        print("Options selected (not implemented)")
                    elif selected_item == 2:
                        return game_state.EXIT
        last_selected = selected_item
        draw_menu()
        pygame.display.flip()
        clock.tick(FPS)

def gameplay_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return game_state.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return game_state.MENU

        screen.fill((0, 100, 0))
        draw_text("Gameplay - Press ESC to return to menu", menu_font, WHITE, 100, SCREEN_HEIGHT // 2)
        pygame.display.flip()
        clock.tick(FPS)

def main():
    current_state = game_state.MENU
    while True:
        if current_state == game_state.MENU:
            current_state = main_menu()
        elif current_state == game_state.CHARACTER_SELECT:
            current_state = character_select_screen()
        elif current_state == game_state.GAMEPLAY:
            current_state = gameplay_loop()
        elif current_state == game_state.EXIT:
            break
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
