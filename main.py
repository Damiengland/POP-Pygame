# Import Modules
import pygame
from player import Player
from spell import Spell
from levels import Levels


# Initialize pygame font library
pygame.font.init()

CUSTOM_FONT = pygame.font.Font("./assets/fonts/Modak-Regular.ttf", 48)

# Fonts
LIVES_FONT = pygame.font.SysFont('arialblack', 32)
FEEDBACK_FONT = pygame.font.SysFont('arialblack', 100)

# Colors
WHITE = (255, 255, 255)


# Screen setup
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pop")
CLOCK = pygame.time.Clock()
FPS = 60


# Load Images
frame_img = pygame.image.load("./assets/images/frame.png")
bg_img = pygame.image.load("./assets/images/BG.png")
start_img, start_img_hover = pygame.image.load("./assets/images/start-screen.png"), \
                             pygame.image.load("./assets/images/start-screen-hover.png")


# EVENTS
PLAYER_HIT = pygame.USEREVENT + 1


# Initialize classes
wizard = Player(WIN)
spells = Spell(WIN, wizard)
levels = Levels(WIN)


# Draw window
def draw_window(lives, level, start_game, time_left):

    WIN.blit(bg_img, (0, 0))

    for spell in spells.spells:
        WIN.blit(spells.spell_img, spell)

    WIN.blit(wizard.current_image, (wizard.x_pos, wizard.y_pos))

    if start_game:

        levels.orbs.draw_orbs()

        pygame.draw.rect(WIN, (160, 80, 245), pygame.Rect(100, 450, 700 * time_left, 50))

        WIN.blit(frame_img, (0, 0))

        lives_text = CUSTOM_FONT.render(f"{str(lives)}", True, WHITE)
        level_text = CUSTOM_FONT.render(f"{str(level)}", True, WHITE)
        WIN.blit(level_text, (37, 75))
        WIN.blit(lives_text, (842, 75))
    else:
        mouse = pygame.mouse.get_pos()
        if 370 < mouse[0] < 530 and 400 < mouse[1] < 460:
            WIN.blit(start_img, (0, 0))
        else:
            WIN.blit(start_img_hover, (0, 0))


# Reset game
def reset_level(level):
    pygame.time.delay(500)
    start_level(level)


def start_level(level):
    wizard.reset()
    if level == 1:
        levels.lvl_1()
    elif level == 2:
        levels.lvl_2()


def next_level():
    if len(levels.orbs.orbs) == 0:
        return True


def timer_bar(current_time, level_time):
    current = current_time
    elapsed_time = current_time - level_time
    time_left = elapsed_time / 30000
    return time_left


# Main game function
def main():

    run = True

    # Game Settings
    lives = 5
    current_time = 0
    level_time = 0

    current_level = 1

    start_game = False

    while run:

        CLOCK.tick(FPS)
        current_time = pygame.time.get_ticks()

        WIN.fill((249, 254, 255))

        time_left = timer_bar(current_time, level_time)

        draw_window(lives, current_level, start_game, time_left)

        if start_game:
            # Get keys user is currently pressing
            keys_pressed = pygame.key.get_pressed()

            wizard.handle_movement(keys_pressed)

            levels.orbs.handle_movement()

            if levels.orbs.player_collision(wizard):
                pygame.event.post(pygame.event.Event(PLAYER_HIT))

            levels.orbs.handle_spell_collision(spells)

            spells.handle_spells()

            if next_level():
                level_time = pygame.time.get_ticks()
                pygame.time.delay(500)
                current_level += 1
                start_level(current_level)

        # Game Over - back to main screen
        if lives == 0:
            start_game = False
            current_level = 1
            lives = 5

        if current_time - level_time > 30000:
            pygame.event.post(pygame.event.Event(PLAYER_HIT))

        pygame.display.update()

        # Check events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                level_time = pygame.time.get_ticks()
                start_level(current_level)
                start_game = True

            if event.type == pygame.KEYDOWN:
                # Check which way player is facing
                if event.key == pygame.K_LEFT:
                    wizard.facing_left = True
                elif event.key == pygame.K_RIGHT:
                    wizard.facing_left = False

                # Check if player shoots spell
                if event.key == pygame.K_SPACE:
                    spells.generate_spell()

            if event.type == PLAYER_HIT:
                reset_level(current_level)
                level_time = pygame.time.get_ticks()
                lives -= 1


# Run game
if __name__ == "__main__":
    main()
