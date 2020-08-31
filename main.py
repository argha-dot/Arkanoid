import sys
import os
import pprint
from random import choices, randrange

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
        self.width  = 60
        self.height = 10
        self.x      = (win_wt//2) - (self.width//2)
        self.y      = win_ht - 50
        self.move   = False
        self.color  = pygame.Color("#c80000")

    def update(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
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
            # self.x = (win_wt//2) - (self.width//2)
            self.y = win_ht - 50
            pygame.mouse.set_pos(self.x, win_ht - 50)
            pos = pygame.mouse.get_pos()
            if 10 < pos[0] < win_wt - self.width - 10:
                self.x = pos[0]
                pygame.mouse.set_pos(self.x, self.y)



class Brick(object):
    def __init__(self, x, y, color):
        self.width  = 50
        self.height = 25
        self.x      = x
        self.y      = y
        self.color  = color
        self.rect   = pygame.Rect(self.x, self.y, self.width, self.height)

    def __str__(self):
        return f"{self.x} {self.y}"

    def update(self):
        pygame.draw.rect(win, self.color, self.rect)


class Drop(object):
    def __init__(self, x, y):
        self.width  = 30
        self.height = 20
        self.type   = choices(["H"])[0]
        self.color  = (randrange(100, 200), randrange(100, 200), randrange(100, 200))
        self.x      = x
        self.y      = y
        self.vel    = 1
        self.rect   = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self):
        pygame.draw.rect(win, self.color, self.rect)
        self.y += self.vel
        

class Level(object):
    # 500, 200 -> 50, 25
    def __init__(self):
        self.level = []
        self.drops = []

    def stages(self):
        list = []
        for i in range(0, 7):
            some = [choices([0, 1])[0] for _ in range(5)]
            some = some + some[::-1]
            list.append(some)
       	return list

    def make_level(self):  
        descriptive_var_name = self.stages()
        
        for line in range(len(descriptive_var_name)):
            color = (randrange(100, 200), randrange(100, 200),  
		     randrange(100, 200))
            
            for brick in range(len(descriptive_var_name[line])):
                if descriptive_var_name[line][brick] == 1:
                    self.level.append(Brick(100 + 52*brick, 50 + 27*line,
		                            color))    
    
        self.drops = choices(self.level, k=randrange(4, 8))

        for x in self.drops:
            print(x)
        
    def update(self):
        for brick in self.level:
            brick.update()
        
        pass


class Ball(object):
    def __init__(self, vel):
        self.vel    = vel 
        self.radius = 3
        self.x      = win_wt//2 - self.radius
        self.y      = win_ht//8 * 7
        self.move   = False
        self.color  = pygame.Color("#c80000")
        self.right  = False
        self.left   = False
        self.up     = False
        self.down   = False

    def update(self, player):
        if self.move:
            
            if (self.right and (not self.left)):
                self.x += self.vel
                if self.x > win_wt - 10:
                    self.right = False; self.left = True

            if (self.left and (not self.right)):
                self.x -= self.vel
                if self.x < 10:
                    self.right = True; self.left = False
            
            if (self.up and (not self.down)):
                self.y -= self.vel
                if self.y < 10:
                    self.up = False; self.down = True

            if self.down and (not self.up):
                self.y += self.vel

        else:
            self.x = player.x + player.width//2
            self.y = win_ht//10 * 9
        gfxdraw.filled_circle(win, self.x, self.y, self.radius*2, self.color)
        self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)


def reset(ball, player):
    if not (ball.move and player.move):
        player.move = True; ball.move = True
        ball.right  = True; ball.left = False
        ball.up     = True; ball.down = False
    else:        
        ball.move   = False; player.move = False


def collision(player, ball, level):

    for i, brick in sorted(enumerate(level.level), reverse=True):
        if ball.rect.colliderect(brick.rect):
            if ball.up and (not ball.down):
                if (ball.rect.top <= brick.rect.bottom <= ball.rect.top + ball.vel):
                    ball.up = False; ball.down = True
                else:
                    if ball.left:
                        ball.left = False; ball.right = True
                    else:
                        ball.right = False; ball.left = True
                        
        if ball.rect.colliderect(brick.rect):
            if ball.down and (not ball.up):
                if (ball.rect.bottom - ball.vel <= brick.rect.top <= ball.rect.bottom):
                    ball.down = False; ball.up = True
                else:
                    if ball.left:
                        ball.left = False; ball.right = True
                    else:
                        ball.right = False; ball.left = True
        
        if ball.rect.colliderect(brick.rect):
            if brick in level.drops:
                print(f"  {brick.x} {brick.y}")
            
            pygame.draw.rect(win, BLACK, brick.rect)
            level.level.pop(i)

    if ball.rect.colliderect(player.rect):
        ball.rect.bottom = player.rect.top
        ball.up = True; ball.down = False
        if ball.right:
            if abs(ball.x - player.x) < 15:
                ball.right = False; ball.left = True

        if ball.left:
            if player.width - 15 < abs(ball.x - player.x) < player.width:
                ball.right = True; ball.left = False

    if not level.level:
        level.make_level()
        pygame.display.update()
        delay(10)   
        reset(ball, player) 

    if ball.y > win_ht + 6:
        delay(5)
        reset(ball, player)


def main():

    def run_game():

        player = Player()
        ball   = Ball(2)
        move   = False
        level  = Level()
        level.make_level()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and \
                   (event.key == K_ESCAPE)):
                    terminate()

                if (event.type == MOUSEBUTTONDOWN and (event.button == 1)) or \
                   (event.type == KEYDOWN and event.key == K_SPACE):
                    reset(ball, player)

            win.fill(BLACK)

            player.update()
            level.update()
            ball.update(player)
            collision(player, ball, level)
            pygame.display.update()
            fps_clock.tick(fps)

    while True:
        run_game()


if __name__ == "__main__":
    main()
