# Import Modules
import pygame


# Orbs
class Orbs:
    def __init__(self, window):
        self.win = window
        self.size = (20, 20)
        self.orbs = []

    def build_orbs(self, strength, start_x, start_y, x_vel=1, y_vel=0, bounce=4, dir_left=False):
        """ Builds a dictionary of orb settings and appends to class array"""
        orb_img = None
        # Set initial direction
        if dir_left:
            initial_x_vel = x_vel * -1
        else:
            initial_x_vel = x_vel
        # Load certain file dependent on orb strength
        if strength == 1:
            self.size = (20, 20)
            orb_img = pygame.transform.scale(
                pygame.image.load("assets/images/orbs/orb_purple.png"), self.size
            ).convert_alpha()
        elif strength == 2:
            self.size = (50, 50)
            orb_img = pygame.transform.scale(
                pygame.image.load("assets/images/orbs/orb_green.png"), (50, 50)
            ).convert_alpha()
        elif strength == 3:
            self.size = (80, 80)
            orb_img = pygame.transform.scale(
                pygame.image.load("assets/images/orbs/orb_blue.png"), self.size
            ).convert_alpha()
        elif strength == 4:
            self.size = (110, 110)
            orb_img = pygame.transform.scale(
                pygame.image.load("assets/images/orbs/orb_yellow.png"), self.size
            ).convert_alpha()
        elif strength == 5:
            self.size = (140, 140)
            orb_img = pygame.transform.scale(
                pygame.image.load("assets/images/orbs/orb_red.png"), self.size
            ).convert_alpha()
        elif strength == 6:
            self.size = (170, 170)
            orb_img = pygame.transform.scale(
                pygame.image.load("assets/images/orbs/orb_black.png"), self.size
            ).convert_alpha()

        mask = pygame.mask.from_surface(orb_img)
        rect = orb_img.get_rect()
        rect[0] = start_x
        rect[1] = start_y
        # Append orb dictionary to self.orbs list
        self.orbs.append({
            "img": orb_img,
            "mask": mask,
            "rect": rect,
            "strength": strength,
            "x_vel": initial_x_vel,
            "y_vel": y_vel,
            "bounce": bounce,
            "s_x": start_x,
            "s_y": start_y,
            "dir_left": dir_left,
        })

    def draw_orbs(self):
        """Draw each orb on window"""
        for orb in self.orbs:
            self.win.blit(orb["img"], orb["rect"])

    def handle_movement(self):
        """Handles movement of each orb"""

        for orb in self.orbs:
            # Bounce Animation
            orb["rect"][1] -= orb["y_vel"]
            if orb["y_vel"] > orb["bounce"] * -1:
                orb["y_vel"] -= 0.1
            if orb["rect"][1] > self.win.get_height() - (50 + orb["rect"].height):
                orb["y_vel"] = orb["bounce"]
            # handle orb collision with walls
            orb["rect"][0] += orb["x_vel"]
            if orb["rect"][0] > self.win.get_width() - (100 + orb["rect"].width):
                orb["x_vel"] = orb["x_vel"] * -1
            if orb["rect"][0] < 100:
                orb["x_vel"] = orb["x_vel"] * -1

    def player_collision(self, player):
        """ Detects collision from each orb with player input"""
        for orb in self.orbs:
            offset = (orb["rect"][0] - player.x_pos, orb["rect"][1] - player.y_pos)
            result = player.player_mask.overlap(orb["mask"], offset)
            if result:
                return True

    def handle_spell_collision(self, spells):
        """ Detects collision with spell and removes or splits ball depending on strength level """
        for spell in spells.spells:
            for orb in self.orbs:
                # Check if collision occurs
                if orb["rect"].colliderect(spell):
                    # remove spell
                    spells.spells = []
                    # reduce strength of orb
                    orb["strength"] -= 1
                    # remove orb
                    if orb["strength"] == 0:
                        self.orbs.remove(orb)
                    # split orb in two
                    else:
                        self.orbs.remove(orb)

                        if orb["rect"].x - orb["rect"].width <= 100:
                            neg_x = 101
                        else:
                            neg_x = orb["rect"].x - orb["rect"].width

                        self.build_orbs(
                            strength=orb["strength"],
                            start_x=orb["rect"].x,
                            start_y=orb["rect"].y,
                            y_vel=orb["bounce"] // 2,
                        )
                        self.build_orbs(
                            strength=orb["strength"],
                            start_x=neg_x,
                            start_y=orb["rect"].y,
                            y_vel=orb["bounce"] // 2,
                            dir_left=True
                        )

    def reset(self):
        """ Resets each orb to original build settings """
        for orb in self.orbs:
            orb["rect"][0] = orb["s_x"]
            orb["rect"][1] = orb["s_y"]
            orb["y_vel"] = 0
            orb["x_vel"] = 1
