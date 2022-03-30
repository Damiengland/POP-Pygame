# Import Modules
import pygame


# Player_old Spell
class Spell:
    def __init__(self, window, player):
        self.win = window
        self.player = player
        self.width = 10

        self.spell_img = pygame.transform.scale(pygame.image.load("assets/images/arrow.png"), (20, 400))
        self.spells = []
        self.vel = 6

    def generate_spell(self):
        spell = pygame.Rect(
            self.player.x_pos + self.player.player_rect.center[0] - self.width // 2,
            self.win.get_height() - 50,
            self.width,
            self.win.get_height() - 50
        )
        if len(self.spells) < 1:
            self.spells.append(spell)

    def handle_spells(self):
        for spell in self.spells:
            spell.y -= self.vel
            if spell.y <= 0:
                self.spells.remove(spell)

