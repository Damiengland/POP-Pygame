# Import Modules
import pygame


# Character
class Player:
    def __init__(self, window):
        self.win = window

        # ANIMATION FRAMES
        # Idle - Facing Left
        self.idle_frames_left = [
            pygame.transform.scale(pygame.image.load('assets/images/anim/idle-anim-1.png'), (40, 50)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('assets/images/anim/idle-anim-2.png'), (40, 50)).convert_alpha(),
        ]
        # Walking - Facing Left
        self.walk_frames_left = [
            pygame.transform.scale(pygame.image.load('assets/images/anim/walk-anim-1.png'), (40, 50)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('assets/images/anim/walk-anim-2.png'), (40, 50)).convert_alpha(),
        ]
        # Idle - facing right
        self.idle_frames_right = []
        for frame in self.idle_frames_left:
            self.idle_frames_right.append(pygame.transform.flip(frame, True, False))
        # Walking - facing right
        self.walk_frames_right = []
        for frame in self.walk_frames_left:
            self.walk_frames_right.append(pygame.transform.flip(frame, True, False))

        # ANIMATION SETTINGS
        self.facing_left = True
        self.current_frame = 0
        self.last_updated = 0
        self.velocity = 0
        self.state = "idle"
        self.current_image = self.idle_frames_left[0]

        # MASK
        self.player_mask = pygame.mask.from_surface(self.idle_frames_left[0])
        self.player_rect = self.idle_frames_left[0].get_rect()
        self.x_pos = self.win.get_width() // 2 - self.player_rect.center[0]
        self.y_pos = window.get_height() - 101

    def handle_movement(self, keys_pressed):
        """Handles movement of player"""
        self.velocity = 0
        if keys_pressed[pygame.K_RIGHT] and self.x_pos < self.win.get_width() - (100 + self.player_rect.center[0] * 2):
            self.velocity = 3
        if keys_pressed[pygame.K_LEFT] and self.x_pos > 100:
            self.velocity = -3
        self.x_pos += self.velocity
        self.set_state()
        self.animate()

    def set_state(self):
        """Determines state depending on the current velocity"""
        self.state = "idle"
        if self.velocity > 0:
            self.state = "right"
        if self.velocity < 0:
            self.state = "left"

    def animate(self):
        """Loops through animation frames in relation to current player state"""
        now = pygame.time.get_ticks()
        if self.state == "idle":
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                if self.facing_left:
                    self.current_image = self.idle_frames_left[self.current_frame]
                elif not self.facing_left:
                    self.current_image = self.idle_frames_right[self.current_frame]
        else:
            if now - self.last_updated > 100:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_left)
                if self.state == "left":
                    self.current_image = self.walk_frames_left[self.current_frame]
                elif self.state == "right":
                    self.current_image = self.walk_frames_right[self.current_frame]

    def reset(self):
        self.x_pos = self.win.get_width() // 2 - self.player_rect.center[0]
