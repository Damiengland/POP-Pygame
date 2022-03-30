# Import Modules
import pygame
from player import Player
from spell import Spell
from levels import Levels


# Initialize pygame font library
pygame.font.init()


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
border_img = pygame.image.load("./assets/images/UI-border.png")
start_img, start_img_hover = pygame.image.load("./assets/images/start-screen.png"), \
                             pygame.image.load("./assets/images/start-screen-hover.png")


# EVENTS
PLAYER_HIT = pygame.USEREVENT + 1


# Initialize classes
wizard = Player(WIN)
spells = Spell(WIN, wizard)
levels = Levels(WIN)


# Draw window
def draw_window(lives, level, start_game):

    WIN.fill((249, 254, 255))

    for spell in spells.spells:
        WIN.blit(spells.spell_img, spell)

    WIN.blit(wizard.current_image, (wizard.x_pos, wizard.y_pos))

    if start_game:
        levels.orbs.draw_orbs()

        WIN.blit(border_img, (0, 0))

        lives_text = LIVES_FONT.render(f"{str(lives)}", True, WHITE)
        level_text = LIVES_FONT.render(f"{str(level)}", True, WHITE)
        WIN.blit(level_text, (37, 75))
        WIN.blit(lives_text, (842, 75))
    else:
        mouse = pygame.mouse.get_pos()
        if 360 < mouse[0] < 560 and 330 < mouse[1] < 400:
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


# Main game function
def main():

    run = True

    # Game Settings
    lives = 5
    timer = 30
    current_level = 1
    start_game = False

    while run:

        CLOCK.tick(FPS)

        draw_window(lives, current_level, start_game)

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
                pygame.time.delay(500)
                current_level += 1
                start_level(current_level)

        # Game Over - back to main screen
        if lives == 0:
            start_game = False
            current_level = 1
            lives = 5

        pygame.display.update()

        # Check events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
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
                lives -= 1


# Run game
if __name__ == "__main__":
    main()
