import pygame
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Volumetric Thermal Expansion")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (130, 130, 130)
BLUE = (70, 130, 180)
RED = (200, 50, 50)
GREEN = (34, 139, 34)
SLIDER_COLOR = (180, 180, 180)
KNOB_COLOR = (60, 60, 60)

# Fonts
font = pygame.font.SysFont(None, 24)

# Ring setup
RING_WIDTH = 120
RING_HEIGHT = 10
RING_GAP = 60
RING_Y = 250
RING_X = (WIDTH - RING_WIDTH) // 2

# Ball properties
MIN_TEMP, MAX_TEMP = 0, 100
MIN_RADIUS, MAX_RADIUS = 20, 40
temperature = 20
ball_radius = MIN_RADIUS
ball_x = WIDTH // 2
ball_start_y = 100
ball_y = float(ball_start_y)
ball_dy = 0.0
falling = False

# Slider
SLIDER_X = 50
SLIDER_Y = 320
SLIDER_WIDTH = 500
KNOB_RADIUS = 10
dragging_knob = False

# Buttons
button_width, button_height = 100, 35
drop_button = pygame.Rect(260, 360, button_width, button_height)
reset_button = pygame.Rect(380, 360, button_width, button_height)

clock = pygame.time.Clock()
FPS = 60


def temp_to_radius(temp):
    return MIN_RADIUS + (temp / MAX_TEMP) * (MAX_RADIUS - MIN_RADIUS)


def temp_to_knob_x(temp):
    return SLIDER_X + (temp / MAX_TEMP) * SLIDER_WIDTH


def knob_x_to_temp(x):
    ratio = (x - SLIDER_X) / SLIDER_WIDTH
    return max(MIN_TEMP, min(MAX_TEMP, ratio * MAX_TEMP))


def draw():
    screen.fill(WHITE)

    # Ring
    pygame.draw.rect(screen, GRAY, (RING_X, RING_Y, RING_WIDTH, RING_HEIGHT))
    pygame.draw.rect(
        screen,
        WHITE,
        (RING_X + (RING_WIDTH - RING_GAP) // 2, RING_Y, RING_GAP, RING_HEIGHT),
    )

    # Ball
    color = RED if ball_radius > RING_GAP / 2 else BLUE
    pygame.draw.circle(screen, color, (ball_x, int(ball_y)), int(ball_radius))

    # Temperature text
    temp_text = font.render(f"Temperature: {int(temperature)}°C", True, BLACK)
    screen.blit(temp_text, (WIDTH // 2 - temp_text.get_width() // 2, 20))

    # Slider
    pygame.draw.rect(screen, SLIDER_COLOR, (SLIDER_X, SLIDER_Y, SLIDER_WIDTH, 4))
    knob_x = int(temp_to_knob_x(temperature))
    pygame.draw.circle(screen, KNOB_COLOR, (knob_x, SLIDER_Y + 2), KNOB_RADIUS)

    # Buttons
    pygame.draw.rect(screen, (50, 160, 100), drop_button)
    pygame.draw.rect(screen, GREEN, reset_button)

    screen.blit(
        font.render("Drop", True, WHITE), (drop_button.x + 25, drop_button.y + 8)
    )
    screen.blit(
        font.render("Reset", True, WHITE), (reset_button.x + 25, reset_button.y + 8)
    )

    pygame.display.flip()


# Main loop
running = True
while running:
    clock.tick(FPS)

    target_radius = temp_to_radius(temperature)
    if abs(ball_radius - target_radius) > 0.1:
        ball_radius += (target_radius - ball_radius) * 0.1

    if falling:
        ball_dy += 0.4
        ball_y += ball_dy

        if ball_y + ball_radius >= RING_Y:
            if ball_radius > RING_GAP / 2:
                ball_y = RING_Y - ball_radius
                falling = False
            elif ball_y - ball_radius > HEIGHT:
                falling = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if drop_button.collidepoint(mx, my):
                if not falling:
                    ball_y = ball_start_y
                    ball_dy = 0
                    falling = True
            elif reset_button.collidepoint(mx, my):
                ball_y = ball_start_y
                ball_dy = 0
                falling = False
                temperature = 20
            elif (
                abs(mx - temp_to_knob_x(temperature)) < KNOB_RADIUS + 2
                and abs(my - (SLIDER_Y + 2)) < KNOB_RADIUS + 2
            ):
                dragging_knob = True

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_knob = False

        elif event.type == pygame.MOUSEMOTION and dragging_knob:
            mx = max(SLIDER_X, min(SLIDER_X + SLIDER_WIDTH, event.pos[0]))
            temperature = knob_x_to_temp(mx)

    draw()

pygame.quit()
sys.exit()
