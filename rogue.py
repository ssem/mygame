import pygame
import random
from human import Human
from pygame.locals import *

class Rogue(Human):
    def __init__(self, x, y):
        super(Rogue, self).__init__(x, y)
        self.speed = 75
        self.spell1_time = 0
        self.spell2_time = 0
        self.spell3_time = 0
        self.spell4_time = 0
        self.spell1_cooldown = 3
        self.spell2_cooldown = 0
        self.spell3_cooldown = 30
        self.spell4_cooldown = 30
        self.image_living = pygame.image.load('images/rogue_live.png')
        self.image_dead = pygame.image.load('images/rogue_dead.png')
        self.image = self.image_living
        self.direction_x = 0
        self.direction_y = 0
        self.stat = 0

    def _patrol(self, time_passed, screen):
        if self.last_move > 2:
            self.last_move = random.randint(0,9) * .1
            self.direction_x = random.randint(-1,1)
            self.direction_y = random.randint(-1,1)
        self.x += time_passed * self.speed * self.direction_x
        self.y += time_passed * self.speed * self.direction_y

    def _kill(self, time_passed, items, screen):
        enemies = self.enemies_in_range(items)
        if len(enemies) < 1:
            self.stat = 0
        else:
            pass

    def _dead(self, time_passed, screen):
        self.image = self.image_dead

    def strike(self):
        base = [20, 100, 200, 300, 400]
        return self.physical_damage(base[self.spell1])

    def resist(self):
        base = [5, 10, 15, 20, 25]
        self._base_resistance = base[self.spell2]
        return 0

    def silence(self):
        base = [2, 3, 4, 5, 6]
        return 0

    def blink(self):
        base = [150, 120, 90, 60, 30]
        return 0
