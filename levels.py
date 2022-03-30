# Import Modules
import pygame
from orbs import Orbs


class Levels:
    def __init__(self, window):
        self.win = window
        self.orbs = Orbs(self.win)

    def lvl_1(self):
        self.orbs.orbs = []
        self.orbs.build_orbs(strength=2, start_x=150, start_y=300)
        self.orbs.build_orbs(strength=2, start_x=700, start_y=300, dir_left=True)

    def lvl_2(self):
        self.orbs.orbs = []
        self.orbs.build_orbs(strength=2, start_x=150, start_y=300)
        self.orbs.build_orbs(strength=2, start_x=700, start_y=300, dir_left=True)
        self.orbs.build_orbs(strength=3, start_x=420, start_y=100, x_vel=0, bounce=7)

