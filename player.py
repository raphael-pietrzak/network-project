


from random import randint
import time

from pygame import Vector2 as vector
import pygame

from  settings import *



class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.display_surface = pygame.display.get_surface()
        self.pos = vector((randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
        self.speed = 400
        self.last_update_time = time.time()
        self.color =  (randint(0, 255), randint(0, 255), randint(0, 255))
        self.inputs = []

    def move(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_update_time
        self.last_update_time = current_time

        if 'up' in self.inputs:
            self.pos.y -= self.speed * time_elapsed
        if 'down' in self.inputs:
            self.pos.y += self.speed * time_elapsed
        if 'left' in self.inputs:
            self.pos.x -= self.speed * time_elapsed
        if 'right' in self.inputs:
            self.pos.x += self.speed * time_elapsed
    
    def get_position(self):
        return [int(self.pos.x), int(self.pos.y)]
    
    def draw(self):
        pygame.draw.rect(self.display_surface, self.color, (self.pos.x, self.pos.y, 40, 40))