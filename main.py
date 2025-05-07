
import pygame
import sys
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()  # For sound effects

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (234, 56, 76)      # Arcade red
BLUE = (37, 99, 235)     # Arcade blue
YELLOW = (234, 179, 8)   # Arcade yellow

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UNTITLED BOXING")
clock = pygame.time.Clock()

# Load assets
try:
    # Load fonts - fallback to default if custom font not available
    try:
        title_font = pygame.font.Font("freesansbold.ttf", 60)
        menu_font = pygame.font.Font("freesansbold.ttf", 36)
    except:
        title_font = pygame.font.SysFont("Arial", 60)
        menu_font = pygame.font.SysFont("Arial", 36)
    
    # Load images
    # You can replace these with actual image paths
    bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img.fill((20, 20, 50))  # Dark blue background as placeholder
    
    # Placeholder for character silhouettes
    left_fighter = pygame.Surface((150, 300))
    left_fighter.fill(BLUE)
    pygame.draw.rect(left_fighter, BLACK, left_fighter.get_rect(), 2)
    
    right_fighter = pygame.Surface((150, 300))
    right_fighter.fill(RED)
    pygame.draw.rect(right_fighter, BLACK, right_fighter.get_rect(), 2)
    
    # Load sounds
    try:
        select_sound = pygame.mixer.Sound("select.wav")  # Replace with actual sound file
        hover_sound = pygame.mixer.Sound("hover.wav")    # Replace with actual sound file
        pygame.mixer.music.load("menu_theme.mp3")        # Replace with actual music file
        pygame.mixer.music.set_volume(0.5)
        sound_loaded = True
    except:
        sound_loaded = False
        print("Sound files could not be loaded. Continuing without sound.")

except Exception as e:
    print(f"Error loading assets: {e}")
    pygame.quit()
    sys.exit()

# Menu options
menu_items = ["START FIGHT", "OPTIONS", "EXIT"]
selected_item = 0
last_selected = 0  # To track changes for sound effects

# Animation variables
animation_counter = 0
pulse_value = 0

def draw_text(text, font, color, x, y, glow=False, glow_color=None, glow_amount=0):
    """Draw text with optional glow effect"""
    if glow:
        glow_surf = font.render(text, True, glow_color)
        glow_rect = glow_surf.get_rect(center=(x, y))
        for offset in range(1, glow_amount + 1):
            screen.blit(glow_surf, (glow_rect.x - offset, glow_rect.y))
            screen.blit(glow_surf, (glow_rect.x + offset, glow_rect.y))
            screen.blit(glow_surf, (glow_rect.x, glow_rect.y - offset))
            screen.blit(glow_surf, (glow_rect.x, glow_rect.y + offset))
    
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    screen.blit(text_surf, text_rect)
    return text_rect

def draw_menu():
    """Draw the main menu"""
    global animation_counter, pulse_value
    
    # Clear screen and draw background
    screen.blit(bg_img, (0, 0))
    
    # Draw fighter silhouettes with floating animation
    y_offset = math.sin(animation_counter * 0.05) * 10
    screen.blit(left_fighter, (50, 250 + y_offset))
    screen.blit(right_fighter, (SCREEN_WIDTH - 200, 250 - y_offset))
    
    # Draw title with glow effect
    pulse_value = (math.sin(animation_counter * 0.1) + 1) * 0.5  # Value between 0 and 1
    glow_amount = int(3 + pulse_value * 5)
    title_color = RED
    draw_text("UNTITLED", title_font, title_color, SCREEN_WIDTH // 2, 100, 
              glow=True, glow_color=YELLOW, glow_amount=glow_amount)
    draw_text("BOXING", title_font, title_color, SCREEN_WIDTH // 2, 170, 
              glow=True, glow_color=YELLOW, glow_amount=glow_amount)
    
    # Draw menu items
    for i, item in enumerate(menu_items):
        if i == selected_item:
            # Selected item has different color and a box
            color = YELLOW
            y_pos = 300 + i * 60
            item_rect = draw_text(item, menu_font, color, SCREEN_WIDTH // 2, y_pos)
            
            # Draw selection box
            box_rect = item_rect.inflate(30, 10)
            pygame.draw.rect(screen, RED, box_rect, 2)
            
            # Draw decorative elements
            pygame.draw.polygon(screen, YELLOW, 
                               [(box_rect.left - 15, box_rect.centery), 
                                (box_rect.left - 5, box_rect.centery - 10),
                                (box_rect.left - 5, box_rect.centery + 10)])
            
            pygame.draw.polygon(screen, YELLOW, 
                               [(box_rect.right + 15, box_rect.centery), 
                                (box_rect.right + 5, box_rect.centery - 10),
                                (box_rect.right + 5, box_rect.centery + 10)])
        else:
            # Non-selected items
            color = WHITE
            draw_text(item, menu_font, color, SCREEN_WIDTH // 2, 300 + i * 60)
    
    # Draw footer text
    footer_font = pygame.font.SysFont("Arial", 16)
    draw_text("© 2025 G19 STUDIOS", footer_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
    
    # Update animation counter
    animation_counter += 1

# Main menu loop
def main_menu():
    global selected_item, last_selected
    
    # Start background music
    if sound_loaded:
        pygame.mixer.music.play(-1)  # Loop indefinitely
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
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
                    
                    # Handle menu selection
                    if selected_item == 0:  # START FIGHT
                        print("Starting the game...")
                        # Here you would transition to the game itself
                        pass
                    elif selected_item == 1:  # OPTIONS
                        print("Opening options menu...")
                        # Here you would open an options submenu
                        pass
                    elif selected_item == 2:  # EXIT
                        print("Exiting game...")
                        running = False
        
        # Record last selected for sound effect triggering
        last_selected = selected_item
        
        # Draw everything
        draw_menu()
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

# Run the menu
if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"Error in main menu: {e}")
    finally:
        pygame.quit()
        sys.exit()
