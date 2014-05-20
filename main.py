#!/usr/bin/env python
import time
import pygame
from mage import Mage
from board import Board
from rogue import Rogue
from warrior import Warrior


class Main():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640,480))
        self.font = pygame.font.SysFont("monospace", 15)
        board = Board()
        mage = Mage(0,0)
        rogue = Rogue(640, 0)
        warrior = Warrior(0, 480)
        self.items = [mage, rogue, warrior]
        self.dead = []

    def start(self):
        old = time.time()
        while True:
            time_passed = time.time() - old
            old = time.time()
            self.screen.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            tmp = []
            for item in self.items:
                item.turn(time_passed, self.items, self.screen)
                self.screen.blit(item.image, (item.x, item.y))
                health = self.font.render(str(item.health),1,(1,1,1))
                x = item.x + item.image.get_width() / 2 - 15
                y = item.y + item.image.get_height() / 2 - 5
                self.screen.blit(health, (x, y))
                if item.health < 1:
                    tmp.append(item)
            for item in tmp:
                self.items.remove(item)
                self.dead.append(item)
            for item in self.dead:
                self.screen.blit(item.image, (item.x, item.y))
                health = self.font.render(str(item.health),1,(1,1,1))
                x = item.x + item.image.get_width() / 2 - 15
                y = item.y + item.image.get_height() / 2 - 5
                self.screen.blit(health, (x, y))

            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.start()
