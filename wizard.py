import pygame
from fighter import Fighter

class Wizard(Fighter): # Inherits from Fighter parent class
    def handle_input(self, key, speed, target):
        dx = 0
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
            # This calls the child's specific overriden attack below
            if key[pygame.K_KP1]:
                self.attack_type = 1
            if key[pygame.K_KP2]:
                self.attack_type = 2
            self.attack(target)
        return dx

    # --- POLYMORPHISM: Method Overriding ---
    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            
            # Ranged Magic Attack Box: huge reach (4x width), but lower damage
            attacking_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip), self.rect.y, 4 * self.rect.width, self.rect.height)
            
            if attacking_rect.colliderect(target.rect):
                target.health -= 7   # Lower damage because it's safer from a distance
                target.hit = True