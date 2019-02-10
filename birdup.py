import pygame, math
from random import randint
from time import sleep

pygame.init()

gravity = 1

def setVariables() :
    global dead
    dead = False
    global score
    score = -2
    global run
    run = True
    global started
    started = False
    global runs
    runs = 0
    global pipes
    pipes = []
    Bird.x = 250
    Bird.y = 250
    Bird.vel = 0

win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Flappy Bird!")
img = pygame.image.load('birdup.png')
bg = pygame.image.load('birdupbg.png')
pipe = pygame.image.load('birduppipe.png')
ground = pygame.image.load('birdupground.png')
font = pygame.font.SysFont('Comic Sans MS', 30)

class Bird :
    x = 250
    y = 250
    vel = 0

    def update() :
        if started :
            if Bird.y < 475 :
                Bird.y += Bird.vel
                Bird.vel += gravity
            else :
                Bird.y = 475
                die()
            if Bird.y < 0 :
                Bird.y = 0
                Bird.vel = 0
        else :
            Bird.y = 250 + math.sin(runs/10)*15
        Bird.getAngle()

    def jump() :
        Bird.vel = -10

    def getAngle() :
        global bird
        bird = pygame.transform.rotate(img, -3*Bird.vel)

class Pipe() :
    def __init__(self, dir, x, len) :
        self.dir = dir
        self.x = x
        self.len = len

    def update(self) :
        if self.dir == "UP" :
            win.blit(pipe, (self.x, 600-self.len))
        else :
            win.blit(pygame.transform.rotate(pipe, 180), (self.x, self.len-431))
        if not dead :
            self.x -= 7

    def checkCollide(self) :
        if self.dir == "DOWN" :
            if Bird.x + 48 > self.x and self.x + 75 > Bird.x :
                if Bird.y + 2 < self.len :
                    die()
        else :
            if Bird.x + 48 > self.x and self.x + 75 > Bird.x :
                if Bird.y + 45 > 600-self.len :
                    die()

def pipePair() :
    r = randint(75, 350)
    pipes.append(Pipe("DOWN", 900, r))
    pipes.append(Pipe("UP", 900, 600-(r+125)))
    global score
    score += 1

def animateGround() :
    win.blit(ground, ((runs%111)*-7, 500))

def die() :
    global dead
    dead = True
    run = False

setVariables()

while run:
    pygame.time.delay(5)
    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                run = False
            elif event.key == pygame.K_SPACE :
                if not started :
                    started = True
                if not dead :
                    Bird.jump()
        elif event.type == pygame.QUIT :
            run = False

    win.blit(bg, (0, 0))
    if runs % 45 == 0 and started :
        pipePair()
    for p in pipes :
        p.update()
        p.checkCollide()
    Bird.update()
    win.blit(bird, (Bird.x,Bird.y))
    animateGround()

    scoreboard = font.render(str(score), False, (0, 0, 0))
    if score > -1 :
        scorebase = pygame.draw.rect(win, (255, 255, 255), (7, 5, len(str(score))*15+10, 35))
        win.blit(scoreboard, (10, 0))
    pygame.display.update()
    if not dead:
        runs += 1

pygame.quit()
