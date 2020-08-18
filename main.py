import sys
import os
import copy

import pygame
from pygame.locals import *

from assets.player import Player
from assets.help import *
from assets.ball import Ball

pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 100"

win_wt, win_ht = 384, 512
fps_clock = pygame.time.Clock()
fps = 60

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
        for i in range(3):
            pygame.draw.rect(win, self.color, self.rect[i])


def main():

    def run_game():

        player = Player(150, 7 * win_ht//8, player_color, 5)
        borders = Border()
        ball = Ball(win_ht, 5)

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
            borders.draw(win)
            # pygame.draw.line(win, (0, 0, 0), (0, player.y), (win_wt, player.y))
            ball.draw(win)
            player.draw(win)

            # Update
            player.update(win, borders)
            ball.update(borders, player)
            pygame.display.flip()
            fps_clock.tick(fps)

    while True:
        run_game()


if __name__ == "__main__":
    main()
