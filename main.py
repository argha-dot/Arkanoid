import sys
import os
import pprint
from random import choice, randrange

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


def delay(j):
    i = 0
    while i < j:
        pygame.time.wait(50)
        i += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                i = j + 1
                terminate()


def fullname(name):
    return os.path.join("data", name)

# ==========================================================================================


win_wt, win_ht = 700, 700
BLACK = pygame.Color("#000000")

fps = 300
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


class Brick(object):
    def __init__(self, x, y, color):
        self.width = 50
        self.height = 25
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        pygame.draw.rect(win, self.color, self.rect)


def stages():
    list = []
    for i in range(0, 7):
        some = [choice([0, 1]) for _ in range(5)]
        some = some + some[::-1]
        list.append(some)
    return list
    # 500, 200 -> 50, 25


class Level(object):
    def __init__(self):
        self.level = []

    def make_level(self):
        descriptive_name = stages()
        for line in range(len(descriptive_name)):
            color = (randrange(100, 200), randrange(100, 200), randrange(100, 200))
            
            for brick in range(len(descriptive_name[line])):
                if descriptive_name[line][brick] == 1:
                    self.level.append(Brick(100 + 52*brick, 50 + 27*line, color))
        
    def update(self):
        for brick in self.level:
            brick.update()
        pass


class Ball(object):
    def __init__(self, vel):
        self.vel = vel 
        self.radius = 3
        self.x = win_wt//2 - self.radius
        self.y = win_ht//8 * 7
        self.move = False
        self.color = pygame.Color("#c80000")
        self.right = False
        self.left = False
        self.up = False
        self.down = False

    def moves(self):
        self.move = True
        self.right = True
        self.left = False
        self.up = True

    def update(self):
        if self.move:
            
            if (self.right and (not self.left)):
                self.x += self.vel
                if self.x > win_wt - 10:
                    self.right = False
                    self.left = True

            if (self.left and (not self.right)):
                self.x -= self.vel
                if self.x < 10:
                    self.right = True
                    self.left = False
            
            if (self.up and (not self.down)):
                self.y -= self.vel
                if self.y < 10:
                    self.up = False
                    self.down = True

            if self.down and (not self.up):
                self.y += self.vel

        else:
            self.x = win_wt//2
            self.y = win_ht//10 * 9
        gfxdraw.filled_circle(win, self.x, self.y, self.radius*2, self.color)
        self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)


def collision(player, ball): 
    if ball.rect.colliderect(player.rect):
        ball.up = True
        ball.down = False
        if ball.right:
            if abs(ball.x - player.x) < 15:
                ball.right = False
                ball.left = True

        if ball.left:
            if player.width - 15 < abs(ball.x - player.x) < player.width:
                ball.right = True
                ball.left = False

    if ball.y > win_ht + 10:
        delay(5)
        ball.move = False
        player.move = False
        ball.down = False


def main():

    def run_game():

        player = Player()
        ball = Ball(2)
        move = False
        level = Level()
        level.make_level()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminate()
                    if event.key == K_SPACE:
                        player.move = True
                        ball.moves()

            win.fill(BLACK)

            player.update()
            ball.update()
            level.update()
            collision(player, ball, level.level)
            pygame.display.update()
            fps_clock.tick(fps)

    while True:
        run_game()


if __name__ == "__main__":
    main()
