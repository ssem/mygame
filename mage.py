import pygame
import random
from human import Human


class Mage(Human):
    def __init__(self, x, y):
        super(Mage, self).__init__(x, y)
        self.image_living = pygame.image.load('images/mage_live.png')
        self.image_dead =  pygame.image.load('images/mage_dead.png')
        self.image = self.image_living
        self.direction_x = 0
        self.direction_y = 0
        self.stat = 0
        self.last_move = 0

    def _patrol(self, time_passed, screen):
        if self.last_move > 2:
            self.last_move = random.randint(-5,5) * .1
            self.direction_x = random.randint(-1,1)
            self.direction_y = random.randint(-1,1)
        self.x += time_passed * self.speed * self.direction_x
        self.y += time_passed * self.speed * self.direction_y

    def _kill(self, time_passed, items, screen):
        enemies = self.enemies_in_range(items)
        if len(enemies) < 1:
            self.stat = 0
        else:
            if self.spell4_time < 0 and len(enemies) > 1:
                for enemy in enemies:
                    enemy.magic_damage(self.lighting())
            elif self.spell2_time < 0 and len(enemies) > 1:
                for enemy in enemies:
                    enemy.magic_damage(self.earthquake())
            elif self.spell1_time < 0:
                target = enemies[0]
                for enemy in enemies[1:]:
                    if target.health < enemy.health:
                        target = enemy
                target.magic_damage(self.fireball())
            elif self.spell3_time < 0 and self.spell2_time < 15:
                target = enemies[0]
                for enemy in enemies[1:]:
                    if target.health > enemy.health:
                        target = enemy
                target.charm_time = self.charm()
            elif self.spell2_time < 0 and self.spell3_time < 10:
                damage = self.earthquake()
                for enemy in enemies:
                    enemy.magic_damage(self.earthquake())
                    enemy.charm_time = 5

        def _dead(self, time_passed, screen):
            self.image = self.image_dead

    def fireball(self):
        self.spell1_time = 5
        base = [10, 100, 200, 300, 400]
        return self.magical_attack(base[self.spell1_level])

    def earthquake(self):
        self.spell2_time = 30
        base = [10, 20, 30, 40, 50]
        return self.magical_attack(base[self.spell2_level])

    def charm(self):
        self.spell3_time = 30
        base = [3, 4, 5, 6, 7]
        return self.magical_attack(base[self.spell3_level])

    def lighting(self):
        self.spell4_time = 180
        base = [100, 150, 200, 250, 300]
        return self.magical_attack(base[self.spell4_level])
