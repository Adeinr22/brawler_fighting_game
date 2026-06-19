import pygame
from fighter import Fighter

class Wizard(Fighter): # Inherits from Fighter parent class
    def handle_input(self, key, speed, target):
        dx = 0
        # Player 2 (Wizard) Controls layout
        if key[pygame.K_LEFT]:
            dx = -speed
            self.running = True
        if key[pygame.K_RIGHT]:
            dx = speed
            self.running = True
        if key[pygame.K_UP] and self.jump == False:
            self.vel_y = -30
            self.jump = True
        if key[pygame.K_KP1] or key[pygame.K_KP2]:
            self.attack(target)
            if key[pygame.K_KP1]:
                self.attack_type = 1
            if key[pygame.K_KP2]:
                self.attack_type = 2
        return dx