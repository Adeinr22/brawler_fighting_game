import pygame
from fighter import Fighter

class Warrior(Fighter): # Inherits from Fighter parent class
    def handle_input(self, key, speed, target):
        dx = 0
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
            if key[pygame.K_r]:
                self.attack_type = 1
            if key[pygame.K_t]:
                self.attack_type = 2
            self.attack(target)
        return dx

    # --- POLYMORPHISM: Method Overriding ---
    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            
            # Heavy Melee Attack Box: short reach (2.3x width), but deals high damage
            attacking_rect = pygame.Rect(self.rect.centerx - (2.3 * self.rect.width * self.flip), self.rect.y, 2.3 * self.rect.width, self.rect.height)
            
            if attacking_rect.colliderect(target.rect):
                target.take_damage(12) 
                target.hit = True