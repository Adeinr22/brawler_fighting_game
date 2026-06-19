import pygame
from fighter import Fighter

class Warrior(Fighter): # Inherits from Fighter parent class
    def handle_input(self, key, speed, target):
        dx = 0
        # Player 1 (Warrior) Controls layout
        if key[pygame.K_a]:
            dx = -speed
            self.running = True
        if key[pygame.K_d]:
            dx = speed
            self.running = True
        if key[pygame.K_w] and self.jump == False:
            self.vel_y = -30
            self.jump = True
        if key[pygame.K_r] or key[pygame.K_t]:
            self.attack(target)
            if key[pygame.K_r]:
                self.attack_type = 1
            if key[pygame.K_t]:
                self.attack_type = 2
        return dx