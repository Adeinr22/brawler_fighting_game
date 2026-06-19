import pygame
from abc import ABC, abstractmethod

# --- THE PARENT CLASS ---
class Fighter(ABC): # <-- Inherit from ABC to make this an Abstract Base Class
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps, sound):
        # All shared attributes remain here
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0: idle | 1: run | 2: jump | 3: attack1 | 4: attack2 | 5: hit | 6: death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0 
        self.attack_sound = sound
        self.hit = False
        # Encapsulation:
        self._health = 100
        self._alive = True

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        
        key = pygame.key.get_pressed()
        
        # The movement conditionals are completely removed from here!
        # Instead, we call a method that the Child classes will handle locally.
        if self.attacking == False and self.alive == True and round_over == False:
            dx = self.handle_input(key, SPEED, target)

        # Apply gravity and physics (shared by both characters)
        self.vel_y += GRAVITY   
        dy += self.vel_y
        
        # Ensure player stays on screen (shared by both characters)
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom
            
        # Face each other (shared)
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
            
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        self.rect.x += dx
        self.rect.y += dy

    # Inside fighter.py:
    def update(self):
        # Check what action the player is performing
        if self._health <= 0:
            self._health = 0
            self._alive = False
            self.update_action(6) # 6: death animation
        elif self.hit == True:
            self.update_action(5) # 5: hit animation
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        # CONTROL ANIMATION COOLDOWN / FRAMERATE DELAY
        # You can increase this number (e.g., 70 or 80) to slow down the hit animation frames specifically!
        animation_cooldown = 50
        
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            if self._alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check if an attack was executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                # Check if the full hit animation finished playing before resetting state
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    # Optional: Lock their next action briefly so they are staggered
                    self.attack_cooldown = 15

    @abstractmethod
    def attack(self, target):
        """Abstract method: Every sub-character must define their own custom hitboxes and damage mechanics."""
        pass

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    @abstractmethod
    def handle_input(self, key, speed, target):
        """Every child character MUST override this method to handle their own keys."""
        pass

    @property
    def health(self):
        return self._health

    # Getter Property: Read-only access to alive status
    @property
    def alive(self):
        return self._alive

    # Setter/Action Method: The ONLY authorized way to modify an object's health state
    def take_damage(self, damage_amount):
        if self._alive:
            self._health -= damage_amount
            self.hit = True
            if self._health <= 0:
                self._health = 0
                self._alive = False