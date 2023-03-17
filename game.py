import pygame, os


pygame.font.init()
pygame.mixer.init()
# MAKE WINDOW FOR GAME
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# COLORS RGB VALUES
BG_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# GAME DEFAULT VALUES
FPS = 60
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
SPACE_DIMENSION = (55, 40)
SHIP_VELOCITY = 7
BULLET_VELOCITY = 10
MAX_BULLETS = 3
# USER DEFINED EVENTS
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
pygame.display.set_caption("First Game")
# FONT FOR POPUP
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)
# USER USED IMAGES
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, SPACE_DIMENSION), 90
)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, SPACE_DIMENSION), 270
)
SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT)
)
# USER DEFINED SOUNDS
BULLET_HIT_SOUND = pygame.mixer.Sound("Assets/Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("Assets/Gun+Silencer.mp3")


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    """Generates all graphics in window

    Args:
        red (pygame.Rect): tracks location of spaceship(red)
        yellow (pygame.Rect): tracks location of spaceship(yellow)
        red_bullets (list): list of bullets of red
        yellow_bullets (list): list of bullets of yellow
        red_health (int)): integer value of red health
        yellow_health (int): integer value of yellow health
    """
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render(f"Health: {str(red_health)}", 1, BG_COLOR)
    yellow_health_text = HEALTH_FONT.render(
        f"Health: {str(yellow_health)}", 1, BG_COLOR
    )
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    pygame.display.update()


def yellow_ship_motion(keys_pressed, yellow):
    """Handles all motions, key control and movement boundary of yellow ship"""
    if keys_pressed[pygame.K_LEFT] and yellow.x - SHIP_VELOCITY > 0:  # LEFT
        yellow.x -= SHIP_VELOCITY
    if (
        keys_pressed[pygame.K_RIGHT]
        and yellow.x + SHIP_VELOCITY + yellow.width < BORDER.x
    ):  # RIGHT
        yellow.x += SHIP_VELOCITY
    if keys_pressed[pygame.K_UP] and yellow.y - SHIP_VELOCITY > 0:  # Up
        yellow.y -= SHIP_VELOCITY
    if (
        keys_pressed[pygame.K_DOWN]
        and yellow.y + SHIP_VELOCITY + yellow.height + 15 < HEIGHT
    ):  # DOWN
        yellow.y += SHIP_VELOCITY


def red_ship_motion(keys_pressed, red):
    """Handles all motions, key control and movement boundary of red ship"""

    if (
        keys_pressed[pygame.K_a] and red.x - SHIP_VELOCITY > BORDER.x + BORDER.width
    ):  # LEFT
        red.x -= SHIP_VELOCITY
    if keys_pressed[pygame.K_d] and red.x + SHIP_VELOCITY + red.width < WIDTH:  # RIGHT
        red.x += SHIP_VELOCITY
    if keys_pressed[pygame.K_w] and red.y - SHIP_VELOCITY > 0:  # UP
        red.y -= SHIP_VELOCITY
    if (
        keys_pressed[pygame.K_s] and red.y + SHIP_VELOCITY + red.height + 15 < HEIGHT
    ):  # DOWN
        red.y += SHIP_VELOCITY


def handle_bullets(yellow_bullets: list, red_bullets, yellow, red):
    """Handles bullet motion and its spaceship collision"""
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text: str):
    """Shows Winner Text(Who Won!) at the game end and delays 5 seconds to start next game"""
    winner_text = WINNER_FONT.render(text, 1, BG_COLOR)
    WIN.blit(
        winner_text,
        (
            WIDTH // 2 - winner_text.get_width() // 2,
            HEIGHT // 2 - winner_text.get_width() // 2,
        ),
    )
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    """Handles fps,pygame.Rect(red and yellow) creation.
    Triggers all other functions to run game properly.
    Calls itself after one game ends to start new game."""
    red = pygame.Rect(700, 300, SPACE_DIMENSION[0], SPACE_DIMENSION[1])
    yellow = pygame.Rect(100, 300, SPACE_DIMENSION[0], SPACE_DIMENSION[1])
    clock = pygame.time.Clock()
    red_bullets = []
    yellow_bullets = []
    red_health, yellow_health = 20, 20
    is_on = True
    while is_on:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_on = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )

                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x + red.width, red.y + red.height // 2 - 2, 10, 5
                    )
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Red Wins"
        if red_health <= 0:
            winner_text = "Yellow Wins"
        if winner_text != "":
            pygame.display.update()
            draw_winner(winner_text)
            break  # someone won
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        keys_pressed = pygame.key.get_pressed()
        yellow_ship_motion(keys_pressed, yellow)
        red_ship_motion(keys_pressed, red)
        handle_bullets(
            yellow_bullets,
            red_bullets,
            yellow,
            red,
        )
    main()


if __name__ == "__main__":
    main()
