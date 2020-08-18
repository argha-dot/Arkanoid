import pygame
from pygame.locals import *

from assets.help import *


class Ball(object):

    def __init__(self, win_ht, vel):
        self.win_ht = win_ht
        self.vel = vel
        self.diameter = 6
        self.x = 150 + 19
        self.y = self.win_ht - 66 - 13
        self.rect = pygame.Rect(self.x, self.y, self.diameter, self.diameter)
        self.color = pygame.Color("#9a7bbc")
        self.img = load_img("ball.png")
        self.move = False
        self.velx = 0
        self.vely = 0
        self.speedx = vel
        self.speedy = vel

    def draw(self, win):
        win.blit(self.img, [self.rect.x, self.rect.centery])

    def update(self, other, player):
        self.velx = 0
        self.vely = 0

        if self.move:
            self.velx += self.speedx
            self.vely -= self.speedy

            self.x += self.velx
            self.rect = pygame.Rect(
                self.x, self.y, self.diameter, self.diameter)
            hits = collisions(self.rect, other.rect)
            for hit in hits:
                if self.velx < 0:
                    self.x = hit.right + 1
                    self.speedx *= -1
                elif self.velx > 0:
                    self.x = hit.x - self.rect.width - 1
                    self.speedx *= -1
            if self.rect.colliderect(player.rect):
                if self.velx > 0:
                    self.x = player.rect.right
                    self.speedx *= -1
                if self.velx < 0:
                    self.x = player.rect.left - self.rect.width
                    self.speedx *= -1

            self.y += self.vely
            self.rect = pygame.Rect(
                self.x, self.y, self.diameter, self.diameter)
            hits = collisions(self.rect, other.rect)
            for hit in hits:
                if self.vely < 0:
                    self.y = hit.bottom
                    self.speedy *= -1
                elif self.vely > 0:
                    self.move = False
                    delay(50, 3)
                    pygame.display.update()
            if self.rect.colliderect(player.rect):
                self.y = player.y - self.diameter
                self.speedy *= -1
        else:
            self.x = player.x + player.width//2 - self.diameter//2
            self.y = self.win_ht - 66 - 13
            self.speedx = self.vel
            self.speedy = self.vel
            self.rect = pygame.Rect(
                self.x, self.y, self.diameter, self.diameter)
