import sys
import os
import random

import pygame
from pygame.locals import *
from pygame import gfxdraw

# ==========================================================================================


def terminate():
    pygame.quit()
    sys.exit()


def out_events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            terminate()


def load_img(name):
    try:
        image = pygame.image.load(fullname(name))
    except pygame.error as e:
        print("Can't load image:", name)
        raise SystemExit(e)
    return image


def fullname(name):
    return os.path.join("data", name)

# ==========================================================================================


win_wt, win_ht = 700, 700
BLACK = pygame.Color("#000000")

fps = 60
fps_clock = pygame.time.Clock()
pygame.init()
pygame.mouse.set_visible(False)
win = pygame.display.set_mode((win_wt, win_ht))


class Player(object):
    def __init__(self):
        self.width = 60
        self.height = 10
        self.x = (win_wt//2) - (self.width//2)
        self.y = win_ht - 50
        self.move = False
        self.color = pygame.Color("#c80000")

    def update(self):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.move:
            pos = pygame.mouse.get_pos()
            if 10 < pos[0] < win_wt - self.width - 10:
                self.x = pos[0]
                pygame.mouse.set_pos(self.x, self.y)
            if win_ht - 250 < pos[1] < win_ht - 10:
                self.y = pos[1]
                pygame.mouse.set_pos(self.x, self.y)
        else:
            self.x = (win_wt//2) - (self.width//2)
            self.y = win_ht - 50
            pygame.mouse.set_pos((win_wt//2) - (self.width//2), win_ht - 50)


class Ball(object):
    def __init__(self):
        self.x = win_wt//2
        self.y = win_ht//4 * 3
        self.radius = 6
        self.move = False
        self.color = pygame.Color("#c80000")

    def update(self):
        if self.move:
            pass
        else:
            self.x = win_wt//2
            self.y = win_ht//4 * 3
        gfxdraw.filled_circle(win, self.x, self.y, 6, self.color)
        self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)


def main():

    def run_game():

        player = Player()
        ball = Ball()
        move = False

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminate()
                    if event.key == K_SPACE:
                        player.move = True
                        ball.move = True

            win.fill(BLACK)

            player.update()
            ball.update()
            pygame.display.update()
            fps_clock.tick(fps)

    while True:
        run_game()


if __name__ == "__main__":
    main()
