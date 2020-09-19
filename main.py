import sys
import os
import pickle
import copy
from time import time
from random import choices, randrange

import pygame
from pygame.locals import *

# ==========================================================================================

# For Graceful Exit
def terminate():
    pygame.quit()
    sys.exit()


# Helps in the Exit
def out_events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            terminate()


# Loads image
def load_img(name):
    try:
        image = pygame.image.load(fullname(name))
    except pygame.error as e:
        print("Can't load image:", name)
        raise SystemExit(e)
    return image


# Delay Script
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


# Full pathname
def fullname(name):
    return os.path.join("data", name)

# ==========================================================================================

win_wt, win_ht = 700, 700
BLACK = pygame.Color("#000000")

fps = 300
fps_clock = pygame.time.Clock()
pygame.init()
pygame.mouse.set_visible(False)   # Sets mouse visibility
win = pygame.display.set_mode((win_wt, win_ht))


# Player class
class Player(object):
    def __init__(self, vel):
        self.width      = 60
        self.height     = 10
        self.x          = (win_wt//2) - (self.width//2)
        self.y          = win_ht - 50
        self.vel        = vel
        self.move       = False
        self.color      = pygame.Color("#c80000")
        self.max_lives  = 3                               # Initial Lives when starting the game
        self.lives      = self.max_lives
        self.score = 0

    def update(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.move:          
            pos = pygame.mouse.get_pos()                        # Gets the mouse position
            if 10 < pos[0] < win_wt - self.width - 10:          # Limits the movement in x-axis
                self.x = pos[0]                              
                pygame.mouse.set_pos(self.x, self.y)
            if win_ht - 250 < pos[1] < win_ht - 10:             # Limits the movement in y-axis
                self.y = pos[1]
                pygame.mouse.set_pos(self.x, self.y)

            keys = pygame.key.get_pressed()           
            if keys[K_a] and self.x > 10:
                self.x -= self.vel
                pygame.mouse.set_pos(self.x, self.y)
            if keys[K_d] and self.x < win_wt - self.width - 10:
                self.x += self.vel
                pygame.mouse.set_pos(self.x, self.y)
            if keys[K_w] and self.y > win_ht - 250:
                self.y -= self.vel
                pygame.mouse.set_pos(self.x, self.y)
            if keys[K_s] and self.y < win_ht - 10:
                self.y += self.vel
                pygame.mouse.set_pos(self.x, self.y)

        else:                                                   # Sets the mouse pos to the 
            self.y = win_ht - 50                                # starting position
            pygame.mouse.set_pos(self.x, win_ht - 50)           
            
            pos = pygame.mouse.get_pos()
            if 10 < pos[0] < win_wt - self.width - 10:
                self.x = pos[0]
                pygame.mouse.set_pos(self.x, self.y)
            
            keys = pygame.key.get_pressed()
            if keys[K_a] and self.x > 10:
                self.x -= self.vel
                pygame.mouse.set_pos(self.x, self.y)
            if keys[K_d] and self.x < win_wt - self.width - 10:
                self.x += self.vel
                pygame.mouse.set_pos(self.x, self.y)

        for i in range(self.lives):     
            pygame.draw.rect(win, (200, 0, 0), [0 + 15*i, 0, 10, 10])


# Brick class
class Brick(object):
    def __init__(self, x, y, color):
        self.width  = 50                                        
        self.height = 25
        self.x      = x
        self.y      = y
        self.color  = copy.deepcopy(color)
        self.move = False
        self.rect   = pygame.Rect(self.x, self.y, self.width, self.height)

    def __str__(self):
        return f"{self.x} {self.y}"

    def update(self, dt):
        pygame.draw.rect(win, self.color, self.rect)
        if self.move:
            pygame.draw.rect(win, self.color, self.rect)
            for x in range(len(self.color)):
                if self.color[x] > 3:
                    self.color[x] -= 3
                else:
                    self.color[x] = 0
            self.y += 3*dt
        self.rect = pygame.Rect(self.x, int(self.y), self.width, self.height)



# Drop item class
class Drop(object):
    def __init__(self, x, y):
        self.width  = 50
        self.height = 25
        self.type   = choices(["H"])[0]                     
        self.color  = [0, 0, randrange(100, 200)]           
        self.x      = x
        self.y      = y
        self.vel    = 1.75
        self.rect   = pygame.Rect(self.x, int(self.y), self.width, self.height)
        self.move   = False
        
    def update(self, dt):
        if self.move:
            pygame.draw.rect(win, self.color, [self.rect.x, self.rect.y, self.rect.width - 5, self.rect.height - 5])
            self.y += self.vel*dt
        self.rect = pygame.Rect(self.x, int(self.y), self.width, self.height)


class Level(object):
    # 500, 200 -> 50, 25
    def __init__(self):
        self.level = []
        self.drops = []
        self.drop_s = []

    def stages(self):
        arr = []
        for i in range(0, 7):
            some = [choices([0, 1])[0] for _ in range(5)]
            some = some + some[::-1]
            arr.append(some)
       	return arr

    def make_level(self):  
        descriptive_var_name = self.stages()
        
        for line in range(len(descriptive_var_name)):
            color = [randrange(50, 200), randrange(50, 200),  
             randrange(50, 200), 255]
            
            for brick in range(len(descriptive_var_name[line])):
                if descriptive_var_name[line][brick] == 1:
                    self.level.append(Brick(100 + 52 * brick, 50 + 27 * line,
		                            color))    
    
        self.drops = choices(self.level, k=randrange(2, 5))
        self.drop_s = [Drop(x.x, x.y) for x in self.drops]

    def update(self, dt):
        for brick in self.level:
            brick.update(dt)

        for i in range(len(self.drop_s)):
            self.drop_s[i].update(dt)
        

class Ball(object):
    def __init__(self, vel):
        self.vel    = vel 
        self.radius = 6
        self.x      = win_wt//2 - self.radius
        self.y      = win_ht//8 * 7
        self.move   = False
        self.hit = False
        self.time = 15
        self.timer = 0
        self.color  = pygame.Color("#c80000")
        self.right  = False
        self.left   = False
        self.up     = False
        self.down   = False

    def update(self, player, dt):
        if self.move:            
            if (self.right and (not self.left)):
                self.x += self.vel*dt
                if self.x > win_wt - 10:
                    self.hit = True
                    self.timer = self.time
                    self.right = False; self.left = True

            if (self.left and (not self.right)):
                self.x -= self.vel*dt
                if self.x < 10:
                    self.hit = True
                    self.timer = self.time
                    self.right = True; self.left = False
            
            if (self.up and (not self.down)):
                self.y -= self.vel*dt
                if self.y < 10:
                    self.hit = True
                    self.timer = self.time
                    self.up = False; self.down = True

            if self.down and (not self.up):
                self.y += self.vel*dt


        else:
            self.x = player.x + player.width//2 - self.radius
            self.y = win_ht//10 * 9
            
        pygame.draw.rect(win, self.color, [int(self.x), int(self.y), self.radius*2, self.radius*2])
        
        self.rect = pygame.Rect(int(self.x), int(self.y), self.radius*2, self.radius*2)


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
            ball.hit = True
            ball.timer = ball.time
            player.score += 10
            if ball.up and (not ball.down):
                if (ball.rect.top <= brick.rect.bottom <= ball.rect.top + ball.vel):
                    ball.up = False; ball.down = True
                else:
                    if ball.left:
                        ball.left = False; ball.right = True
                    else:
                        ball.right = False; ball.left = True

            else :
                if (ball.rect.bottom - ball.vel <= brick.rect.top <= ball.rect.bottom):
                    ball.down = False; ball.up = True
                else:
                    if ball.left:
                        ball.left = False; ball.right = True
                    else:
                        ball.right = False; ball.left = True
        
        # if ball.rect.colliderect(brick.rect):     
            brick.move = True

        
    for i, drop in sorted(enumerate(level.drop_s), reverse=True):
        if ball.rect.colliderect(drop.rect):
            drop.move = True

    for i, drop in sorted(enumerate(level.drop_s), reverse=True):
        if player.rect.colliderect(drop.rect) and drop.move:
            player.lives += 1
            player.score += 50
            drop.move = False
            pygame.draw.rect(win, BLACK, drop.rect)
            level.drop_s.pop(i)

            
    if ball.rect.colliderect(player.rect):
        ball.rect.bottom = player.rect.top
        ball.hit = True
        ball.timer = ball.time
        ball.up = True; ball.down = False
        if ball.right:
            if abs(ball.x - player.x) < 10:
                ball.right = False; ball.left = True

        if ball.left:
            if player.width - 10 < abs(ball.x - player.x) < player.width:
                ball.right = True; ball.left = False

    if not level.level:
        level.make_level()
        pygame.display.update()
        delay(10)   
        reset(ball, player) 

    if ball.y > win_ht + 6:
        delay(5)
        player.score -= 100
        player.lives -= 1
        reset(ball, player)


def main():

    def start_screen():

        while True:
            
            pass

        win.fill((0, 0, 0))

    def game_over(score):
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and
                   (event.key == K_ESCAPE)):
                    terminate()

                if event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_SPACE):
                    return
            
            win.fill((0, 0, 0))

            text_font  = pygame.font.SysFont("comicsans", 45)

            text       = text_font.render("Game Over", True, (50, 50, 50))
            score_text = text_font.render(f"{score}", True, (50, 50, 50))
            
            text_rect  = text.get_rect()
            score_rect = score_text.get_rect()
            
            win.blit(text,       (win_wt//2 -  text_rect.width//2, 100))
            win.blit(score_text, (win_wt//2 - score_rect.width//2, 200))

            pygame.display.update()

    def run_game():
        global fps

        player = Player(4)
        ball   = Ball(4)
        level  = Level()
        level.make_level()

        last_time = time()

        print(len(level.level))

        while True:
            dt = time() - last_time
            dt *= 120
            last_time = time()

            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()

                if event.type == KEYDOWN and (event.key == K_ESCAPE):
                    terminate()

                if event.type == KEYDOWN and (event.key == K_e):
                    fps = 10
                    
                if event.type == KEYUP and (event.key == K_e):
                    fps = 300

                if (event.type == MOUSEBUTTONDOWN and (event.button == 1)) or \
                   (event.type == KEYDOWN and event.key == K_SPACE):
                    reset(ball, player)

            win.fill(BLACK)

            player.update()
            level.update(dt)
            ball.update(player, dt)
            collision(player, ball, level)

            score_font = pygame.font.SysFont("comicsans", 25)
            score      = score_font.render(f"{player.score}", True, (150, 150, 150))
            score_rect = score.get_rect()
            win.blit(score, (win_wt - score_rect.width, 0))

            if player.lives < 0:
                pygame.display.update()
                delay(10)
                game_over(player.score)
                return
                
            if ball.timer > 0:
                ball.timer -= 1

            if ball.timer:
                ball.color = pygame.Color("#c86464")
                ball.radius = 10
            else:
                ball.color = pygame.Color("#c80000")
                ball.radius = 6

            for i, brick in sorted(enumerate(level.level), reverse=True):
                if brick.color[0] == 0:
                    level.level.pop(i)

            pygame.display.update()
            fps_clock.tick(fps)


    while True:
        # game_over()
        run_game()


if __name__ == "__main__":
    main()
