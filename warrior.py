import pygame
import random
from human import Human


class Warrior(Human):
    def __init__(self, x, y):
        super(Warrior, self).__init__(x, y)
        self.modify = 1
        self.modify_time = 0
        self.image_living = pygame.image.load('images/warrior_live.png')
        self.image_dead = pygame.image.load('images/warrior_dead.png')
        self.image = self.image_living
        self.direction_x = 0
        self.direction_y = 0
        self.stat = 0
        self.last_move = 0

    def _patrol(self, time_passed, screen):
        self.modify_time -= time_passed
        if self.last_move > 2:
            self.last_move = random.randint(-9,0) * .1
            self.direction_x = random.randint(-1,1)
            self.direction_y = random.randint(-1,1)
        self.x += time_passed * self.speed * self.direction_x
        self.y += time_passed * self.speed * self.direction_y

    def _kill(self, time_passed, items, screen):
        self.modify_time -= time_passed
        enemies = self.enemies_in_range(items)
        if len(enemies) < 1:
            self.state = 0
        else:
            pass

    def _dead(self, time_passed, screen):
        self.image = self.image_dead

    def charge(self):
        base = [1,2,3,4,5]
        if self.modify_time > 0:
            base = [1 * self.modify,
                    2 * self.modify,
                    3 * self.modify,
                    4 * self.modify,
                    5 * self.modify]
        return int(base[self.spell1])

    def strike(self):
        base = [20, 120, 140, 360, 500]
        if self.modify_time > 0:
            base = [20 * self.modify,
                    120 * self.modify,
                    240 * self.modify,
                    360 * self.modify,
                    500 * self.modify]
        return self.physical_damage(int(base[self.spell2]))

    def rage(self):
        base = [2, 3, 4, 5, 6]
        self.modify = base[self.spell3]
        self.modify_time = 15
        return 0

    def fortify(self):
        base = [100, 200, 300, 400, 500]
        self.base_health = base[self.spell4]
        return 0

