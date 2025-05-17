import pygame
import game_state

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (234, 56, 76)
BLUE = (37, 99, 235)
YELLOW = (234, 179, 8)
GRAY = (100, 100, 100)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

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

def draw_stars(surface, x, y, count):
    for i in range(5):
        color = YELLOW if i < count else GRAY
        pygame.draw.polygon(surface, color, [
            (x + i * 22 + 10, y),
            (x + i * 22 + 14, y + 14),
            (x + i * 22 + 24, y + 14),
            (x + i * 22 + 16, y + 22),
            (x + i * 22 + 18, y + 34),
            (x + i * 22 + 10, y + 26),
            (x + i * 22 + 2, y + 34),
            (x + i * 22 + 4, y + 22),
            (x + i * 22 - 4, y + 14),
            (x + i * 22 + 6, y + 14)
        ])

def character_select_screen(screen, clock):
    font = pygame.font.SysFont("Arial", 24)
    big_font = pygame.font.SysFont("Arial", 32)
    current_index = 0
    transition_offset = 0
    transitioning = False
    transition_speed = 40

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return game_state.EXIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return game_state.MENU
                elif event.key == pygame.K_RETURN:
                    print("Character selected:", characters[current_index]["name"])
                    return game_state.GAMEPLAY
                elif not transitioning:
                    if event.key == pygame.K_RIGHT:
                        transitioning = True
                        transition_offset = -SCREEN_WIDTH
                        current_index = (current_index + 1) % len(characters)
                    elif event.key == pygame.K_LEFT:
                        transitioning = True
                        transition_offset = SCREEN_WIDTH
                        current_index = (current_index - 1) % len(characters)

        screen.fill(BLACK)

        char = characters[current_index]

        portrait_rect = pygame.Rect(50 + transition_offset, 100, 250, 400)
        pygame.draw.rect(screen, char["portrait_color"], portrait_rect)
        pygame.draw.rect(screen, WHITE, portrait_rect, 3)

        text_x = 350 + transition_offset
        screen.blit(big_font.render(char["name"], True, YELLOW), (text_x, 100))

        backstory_lines = font.render(char["backstory"][:90] + "...", True, WHITE)
        screen.blit(backstory_lines, (text_x, 150))

        screen.blit(font.render("Passive: " + char["passive"], True, WHITE), (text_x, 250))
        draw_stars(screen, text_x + 120, 240, char["stars"]["passive"])

        screen.blit(font.render("Special: " + char["special"], True, WHITE), (text_x, 320))
        draw_stars(screen, text_x + 120, 310, char["stars"]["special"])

        screen.blit(font.render("Use <- or -> to navigate, ENTER to select", True, GRAY), (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 50))

        if transitioning:
            transition_offset = int(transition_offset * 0.8)
            if abs(transition_offset) < 5:
                transition_offset = 0
                transitioning = False

        pygame.display.flip()
        clock.tick(FPS)

    return game_state.GAMEPLAY
