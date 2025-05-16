import pygame
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Volumetric Thermal Expansion (Side View)")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (220, 20, 60)
GRAY = (120, 120, 120)
GREEN = (34, 139, 34)

# Fonts
font = pygame.font.SysFont(None, 28)

# Ring settings
RING_WIDTH = 120
RING_HEIGHT = 10
RING_Y = 250
RING_X = (WIDTH - RING_WIDTH) // 2
RING_GAP = 60

# Ball settings
MIN_RADIUS = 20
MAX_RADIUS = 40
MIN_TEMP = 0
MAX_TEMP = 100
temperature = 20
TEMP_STEP = 10
ball_radius = MIN_RADIUS
ball_x = WIDTH // 2
initial_ball_y = 100.0
ball_y = initial_ball_y
ball_dy = 0.0
falling = False

# Buttons
button_width = 100
button_height = 40
heat_button = pygame.Rect(40, 330, button_width, button_height)
cool_button = pygame.Rect(160, 330, button_width, button_height)
drop_button = pygame.Rect(280, 330, button_width, button_height)
reset_button = pygame.Rect(400, 330, button_width, button_height)

# Clock
clock = pygame.time.Clock()
FPS = 60


def temperature_to_radius(temp):
    return MIN_RADIUS + (temp / MAX_TEMP) * (MAX_RADIUS - MIN_RADIUS)


def draw_scene():
    screen.fill(WHITE)

    # Draw ring
    pygame.draw.rect(screen, GRAY, (RING_X, RING_Y, RING_WIDTH, RING_HEIGHT))
    pygame.draw.rect(
        screen,
        WHITE,
        (RING_X + (RING_WIDTH - RING_GAP) // 2, RING_Y, RING_GAP, RING_HEIGHT),
    )

    # Ball color changes based on size
    color = RED if ball_radius > RING_GAP // 2 else BLUE
    pygame.draw.circle(screen, color, (ball_x, int(ball_y)), int(ball_radius))

    # Temperature display
    temp_text = font.render(f"Temperature: {temperature}°C", True, BLACK)
    screen.blit(temp_text, (WIDTH // 2 - temp_text.get_width() // 2, 20))

    # Buttons
    pygame.draw.rect(screen, (200, 50, 50), heat_button)
    pygame.draw.rect(screen, (50, 100, 200), cool_button)
    pygame.draw.rect(screen, (50, 180, 100), drop_button)
    pygame.draw.rect(screen, GREEN, reset_button)

    screen.blit(
        font.render("Heat", True, WHITE), (heat_button.x + 25, heat_button.y + 8)
    )
    screen.blit(
        font.render("Cool", True, WHITE), (cool_button.x + 25, cool_button.y + 8)
    )
    screen.blit(
        font.render("Drop Ball", True, WHITE), (drop_button.x + 5, drop_button.y + 8)
    )
    screen.blit(
        font.render("Reset", True, WHITE), (reset_button.x + 20, reset_button.y + 8)
    )

    pygame.display.flip()


# Game loop
running = True
while running:
    clock.tick(FPS)

    # Smooth radius animation
    target_radius = temperature_to_radius(temperature)
    if abs(ball_radius - target_radius) > 0.1:
        ball_radius += (target_radius - ball_radius) * 0.1

    # Ball falling physics
    if falling:
        ball_dy += 0.5
        ball_y += ball_dy

        if ball_y + ball_radius >= RING_Y:
            if ball_radius > RING_GAP // 2:
                ball_y = RING_Y - ball_radius
                falling = False
            elif ball_y - ball_radius > HEIGHT:
                falling = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if heat_button.collidepoint(event.pos):
                if temperature < MAX_TEMP:
                    temperature += TEMP_STEP
            elif cool_button.collidepoint(event.pos):
                if temperature > MIN_TEMP:
                    temperature -= TEMP_STEP
            elif drop_button.collidepoint(event.pos):
                if not falling:
                    ball_y = initial_ball_y
                    ball_dy = 0
                    falling = True
            elif reset_button.collidepoint(event.pos):
                ball_y = initial_ball_y
                ball_dy = 0
                falling = False
                temperature = 20

    draw_scene()

pygame.quit()
sys.exit()
