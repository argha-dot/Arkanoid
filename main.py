import pygame
import sys, os
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


win_wt, win_ht = 700, 700
BLACK = pygame.Color("#000000")

fps = 60
fps_clock = pygame.time.Clock()
pygame.init()
pygame.mouse.set_visible(False)
win = pygame.display.set_mode((win_wt, win_ht))


class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 10
        self.color = pygame.Color("#c82929")
    
    def update(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pos = pygame.mouse.get_pos()
        if 10 < pos[0] < win_wt - self.width - 10:
            self.x = pos[0]
            pygame.mouse.set_pos(self.x, self.y)
        if win_ht - 100 < pos[1] < win_ht - 10:
            self.y = pos[1]
            pygame.mouse.set_pos(self.x, self.y)


def main():

    def run_game():

        player = Player(200, win_ht - 50)

        while True:
            out_events()
            win.fill(BLACK)

            player.update()
            pygame.display.update()
            dt = fps_clock.tick(fps) / 1000

    while True:
        run_game()


if __name__ == "__main__":
    main()


