import sys
import os

import pygame
from pygame.locals import *

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

bg = pygame.Color("#2c2137")
player_color = pygame.Color("#764462")

# ==========================================================================================


pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "1, 1"

win_wt, win_ht = 384, 512
fps_clock = pygame.time.Clock()
fps = 120

win = pygame.display.set_mode((win_wt, win_ht))


class Player(object):

    def __init__(self, x, y):
        self.width = 50
        self.height = 15
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = player_color
        self.vel = 0
        self.speed = 4
        self.left = False
        self.right = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update(self):
        self.vel = 0
        if self.left and not self.right and (self.x > 0):
            self.vel = -self.speed
        if self.right and not self.left and (self.x < (win_wt - self.width)):
            self.vel = self.speed

        self.x += self.vel

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


def main():

    def run_game():

        player = Player(150, win_ht - 66)

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

            win.fill(bg)
            player.draw(win)

            player.update()
            pygame.display.flip()
            fps_clock.tick(fps)

    while True:
        run_game()


if __name__ == "__main__":
    main()
