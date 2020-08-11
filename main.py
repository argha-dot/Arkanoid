import sys
import os

import pygame
from pygame.locals import *

#==========================================================================================


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


#==========================================================================================

bg = load_img("bg.png")
player_img = load_img(("player.png"))

#==========================================================================================


pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "1, 1"

win_wt, win_ht = 384, 384
fps_clock = pygame.time.Clock()
fps = 60

win = pygame.display.set_mode((win_wt, win_ht))

class Player(object):

    def __init__(self, x, y):
        self.img = player_img
        self.rect = player_img.get_rect()
        self.rect.top = x
        self.rect.left = y
        self.x = self.rect.top
        self.y = self.rect.left
        self.vel = 5

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


def main():

    def run_game():

        player = Player(150, win_ht - 66)

        while True:
            out_events()

            win.blit(bg, [0, 0])
            player.draw(win)
            keys = pygame.key.get_pressed()
            

            pygame.display.update()
            dt = fps_clock.tick(fps) / 1000

    while True:
        run_game()


if __name__ == "__main__":
    main()
