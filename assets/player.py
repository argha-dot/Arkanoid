import random

import pygame
from pygame.locals import *

from assets.particles import Particles
from assets.help import *


class Player(object):

    def __init__(self, x, y, color):
        self.width = 50
        self.height = 10
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = color
        self.vel = 0
        self.speed = 5
        self.left = False
        self.right = False
        self.boost_right = \
            Particles(self.x + self.width, self.y +
                      self.height - 5, 100, 2.5, color)
        self.boost_left = \
            Particles(self.x, self.y + self.height - 5, 100, 2.5, color)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update(self, win, other):
        self.vel = 0

        if self.left and not self.right:
            self.vel += -self.speed
        if self.right and not self.left:
            self.vel += self.speed

        self.x += self.vel
        self.boost_right.x = self.x + self.width - 10
        self.boost_left.x = self.x + 10
        self.boost_right.update(win)
        self.boost_left.update(win)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        hits = collisions(self.rect, other.rect)
        for hit in hits:
            if self.vel > 0:
                self.x = hit.left - self.width
            elif self.vel < 0:
                self.x = hit.right
