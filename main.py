import sys
import os

import pygame
from pygame.locals import *

from assets.player import Player
from assets.help import *

# ==========================================================================================

bg = pygame.Color("#001b2e")
player_color = pygame.Color("#2d757e")

# ==========================================================================================


pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 100"

win_wt, win_ht = 384, 512
fps_clock = pygame.time.Clock()
fps = 120

win = pygame.display.set_mode((win_wt, win_ht), NOFRAME)


class Border(object):
    def __init__(self):
        self.rect = [pygame.Rect(5, 0, 5, win_ht),
                     pygame.Rect(win_wt - 10, 0, 5, win_ht), 
                     pygame.Rect(5, 35, win_wt - 10, 5)]
        self.color = pygame.Color("#9a7bbc")

    def draw(self, win):
        for side in self.rect:
            pygame.draw.rect(win, self.color, side)


class Ball(object):
    
    def __init__(self):
        self.diameter = 6
        self.x = 150 - 3
        self.y = win_ht - 66 - 6
        self.rect = pygame.Rect(150 - 3, in_ht - 66 - 6, self.diameter, self.diameter)
        self.color = pygame.Color("#9a7bbc")
        self.move = False
        self.vel = 0
        self.speed = 6

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update(self):
        pass


def main():

    def run_game():

        player = Player(150, 7 * win_ht//8, player_color)
        borders = Border()

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

            # Draw
            win.fill(bg)
            player.draw(win)
            borders.draw(win)

            # Update
            player.update(win, borders)
            pygame.display.flip()
            fps_clock.tick(fps)

    while True:
        run_game()


if __name__ == "__main__":
    main()
