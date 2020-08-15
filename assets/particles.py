import random

import pygame
from pygame.locals import *


class Particle(object):
    def __init__(self, x, y, vel, color):
        self.x = x
        self.y = y
        self.color = color
        self.vel = vel
        self.radius = random.randint(1, 6)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(
            self.x), int(self.y)), int(self.radius))


class Particles(object):
    def __init__(self, x, y, n, vel, color):
        self.x = x
        self.y = y
        self.vel = vel
        self.nums = n
        self.color = color
        self.particles = [Particle(self.x, self.y, self.vel, self.color) for _ in range(n)]

    def draw(self, win):
        for p in self.particles:
            p.draw(win)

    def update(self, win):
        while len(self.particles) < self.nums:
            self.particles.append(Particle(self.x, self.y, self.vel, self.color))

        for i, p in sorted(enumerate(self.particles), reverse=True):
            p.x -= random.randint(-2, 2)
            p.y += p.vel
            p.radius -= 0.3
            p.draw(win)
            if p.radius < 1:
                self.particles.pop(i)

