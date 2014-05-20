import math
import random

class Human(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.last_move = 0
        self.image = None
        self.speed = 50
        self.items = {'helm':None,
                      'neck':None,
                      'shoulders':None,
                      'chest':None,
                      'gloves':None,
                      'legs':None,
                      'boots':None,
                      'ring':None,
                      'mainhand':None,
                      'offhand':None}
        self._base_health = 295
        self._base_mana = 100
        self._base_strength = 5
        self._base_intellect = 5
        self._base_agility = 5
        self._base_crit = 1
        self._base_dodge = 1
        self._base_armor = 10
        self._base_resistance = 10

        self.health_used = 0
        self.mana_used = 0

        self.charm_time = 0
        self.silence_time = 0
        self.taunt_time = 0

        self.spell1_time = 0
        self.spell2_time = 0
        self.spell3_time = 0
        self.spell4_time = 0

        self.spell1_level = 1
        self.spell2_level = 1
        self.spell3_level = 1
        self.spell4_level = 1

    @property
    def health(self):
        health = self._base_health + self.strength - self.health_used
        if health < 0:
            return 0
        return health

    @property
    def mana(self):
        mana = self._base_mana + self.intellect - self.mana_used
        if mana < 0:
            return 0
        return mana

    @property
    def strength(self):
        return self._base_strength + self.retrieve_stats('strength')

    @property
    def intellect(self):
        return self._base_intellect + self.retrieve_stats('intellect')

    @property
    def agility(self):
        return self._base_agility + self.retrieve_stats('agility')

    @property
    def crit(self):
        return self._base_crit + self.retrieve_stats('crit')

    @property
    def dodge(self):
        return self._base_dodge + self.retrieve_stats('dodge')

    @property
    def armor(self):
        return self._base_armor + self.retrieve_stats('armor')

    @property
    def resistance(self):
        return self._base_resistance + self.retrieve_stats('resistance')

    def turn(self, time_passed, items, screen):
        self.charm_time -= time_passed
        self.silence_time -= time_passed
        self.taunt_time -= time_passed
        self.last_move += time_passed
        if self.health < 1:
            self.dead(time_passed, screen)
            self.stat = 3
        if self.stat == 0 and self.charm_time < 0 and self.taunt_time < 0:
            self.patrol(time_passed, items, screen)
        elif self.stat == 1 and self.charm_time < 0 and self.silence_time < 0:
            self.kill(time_passed, items, screen)

    def patrol(self, time_passed, items, screen):
        self._patrol(time_passed, screen)
        max_x = screen.get_width() - self.image.get_width()
        max_y = screen.get_height() - self.image.get_height()
        if self.x > max_x:
            self.x = max_x
        elif self.x < 0:
            self.x = 0
        if self.y > max_y:
            self.y = max_y
        elif self.y < 0:
            self.y = 0
        for item in items:
            x = abs(self.x - item.x)
            y = abs(self.y - item.y)
            distance = math.sqrt(x ** 2 + y ** 2)
            if distance != 0 and distance < 175:
                self.stat = 1

    def kill(self, time_passed, items, screen):
        self.spell1_time -= time_passed
        self.spell2_time -= time_passed
        self.spell3_time -= time_passed
        self.spell4_time -= time_passed
        self._kill(time_passed, items, screen)

    def dead(self, time_passed, screen):
        self._dead(time_passed, screen)

    def enemies_in_range(self, items):
        enemies = []
        for item in items:
            x = abs(self.x - item.x)
            y = abs(self.y - item.y)
            distance = math.sqrt(x ** 2 + y ** 2)
            if distance != 0 and distance < 175:
                enemies.append(item)
        return enemies

    def retrieve_stats(self, stat_type):
        response = 0
        for item in self.items:
            if self.items[item]:
                response += self.items[item][stat_type]
        return response

    def physical_attack(self, base):
        sway = random.randint(-10,10) + 100
        if random.randint(0,100) < self.crit:
            sway += random.randint(0,30)
        return int((base + self.strength + (self.agility * 2)) * (sway * .01))

    def magical_attack(self, base):
        sway = random.randint(-10,10) + 100
        if random.randint(0,100) < self.crit:
            sway += random.randint(0,30)
        return int((base + self.intellect) * (sway * .01))

    def physical_damage(self, damage):
        if random.randint(0,100) > self.dodge:
            self.health_used += (damage - self.armor)

    def magic_damage(self, damage):
        if random.randint(0,100) > self.dodge:
            self.health_used += (damage - self.resistance)
