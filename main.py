import sys
import os

import pygame
from pygame.locals import *

from assets.player import Player
from assets.help import *

pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 100"

win_wt, win_ht = 384, 512
fps_clock = pygame.time.Clock()
fps = 120

win = pygame.display.set_mode((win_wt, win_ht), NOFRAME)


# ==========================================================================================

bg = pygame.Color("#001b2e")
player_color = pygame.Color("#2d757e")
font = pygame.font.SysFont("Arial", 18)

# ==========================================================================================


class Border(object):
    def __init__(self):
        self.rect = [pygame.Rect(5, 0, 5, win_ht),
                     pygame.Rect(win_wt - 10, 0, 5, win_ht), 
                     pygame.Rect(5, 35, win_wt - 10, 5),
                     pygame.Rect(5, win_ht - 5, win_wt, 5)]
        self.color = pygame.Color("#9a7bbc")

    def draw(self, win):
        for side in self.rect:
            pygame.draw.rect(win, self.color, side)


class Ball(object):
    
    def __init__(self):
        self.diameter = 6
        self.x = 150 + 19
        self.y = win_ht - 66 - 13
        self.rect = pygame.Rect(self.x, self.y, self.diameter, self.diameter)
        self.color = pygame.Color("#9a7bbc")
        self.img = load_img("ball.png")
        self.move = False
        self.velx = 0
        self.vely = 0
        self.speedx = 4
        self.speedy = 4

    def draw(self, win):
        win.blit(self.img, [self.rect.x, self.rect.centery])

    def update(self, other, player):
        self.velx = 0
        self.vely = 0
        
        if self.move:    
            self.velx += self.speedx
            self.vely -= self.speedy

        self.x += self.velx
        self.rect = pygame.Rect(self.x, self.y, self.diameter, self.diameter)
        hits = collisions(self.rect, other.rect)
        for hit in hits:
            if self.velx < 0:
                self.x = hit.right
                self.speedx *= -1
            elif self.velx > 0:
                self.x = hit.x - self.rect.width
                self.speedx *= -1
        if self.rect.colliderect(player.rect):
            if self.velx > 0:
                self.x = player.rect.right
                self.speedx *= -1
            if self.velx < 0:
                self.x = player.rect.left - self.rect.width
                self.speedx *= -1

        self.y += self.vely
        self.rect = pygame.Rect(self.x, self.y, self.diameter, self.diameter)
        hits = collisions(self.rect, other.rect)
        for hit in hits:
            if self.vely < 0:
                self.y = hit.bottom
                self.speedy *= -1
            elif self.vely > 0:
                self.y = hit.top - self.rect.height
                self.speedy *= -1
        if self.rect.colliderect(player.rect):
            self.y = player.rect.top - self.rect.height
            self.speedy *= -1


def main():

    def run_game():

        player = Player(150, 7 * win_ht//8, player_color)
        borders = Border()
        ball = Ball()

        while True:

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    terminate()
                if event.type == KEYDOWN:
                    if (event.key == K_LEFT) or (event.key == K_a):
                        player.left = True
                    if (event.key == K_RIGHT) or (event.key == K_d):
                        player.right = True

                if event.type == KEYUP:
                    if event.key == K_LEFT or (event.key == K_a):
                        player.left = False
                    if event.key == K_RIGHT or (event.key == K_d):
                        player.right = False
                    if event.key == K_SPACE:
                        ball.move = True

            # Draw
            win.fill(bg)
            win.blit(update_fps(fps_clock, font), (10, 0))
            player.draw(win)
            borders.draw(win)
            ball.draw(win)

            # Update
            player.update(win, borders)
            ball.update(borders, player)
            pygame.display.flip()
            fps_clock.tick(fps)

    while True:
        run_game()


if __name__ == "__main__":
    main()
