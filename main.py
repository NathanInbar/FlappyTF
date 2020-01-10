import pygame
import sys , time , os, threading
import math
from random import randint
import numpy as np
#for pipe spawning
from apscheduler.schedulers.background import BackgroundScheduler

pygame.init()
#Constants
WIDTH = 800
HEIGHT = 600
#4:3 aspect ratio
fps = 120
G = -.4
spawn_time = 1.5
background_color = (43,42,42)#dark grey
#end constants

screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Flappy Bird TF -- Justin && Nathan")
clock = pygame.time.Clock()

#for pipe spawning
sched = BackgroundScheduler()
sched.start()
#end pipe spawning

birds = []
pipes = []

class Bird:
    def __init__(self):
        self.pos = (100,150)
        self.v = 0
        self.size = 25
        self.jump_force = 9
        self.color = (200,200,5)#yellow
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size,self.size)
    def update(self):

        self.pos = (self.pos[0],self.pos[1] - self.v)  #changes our position based  on our velocity every frame
        self.v += G #changes our velocity due to gravity G

        if (self.check_collision() == 1): # we are dead
            print('signal the NN that this bird ate shit')
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size,self.size)
        #keep bottom
        self.render()#draw to screen
    def render(self):#draw our bird to screen
        pygame.draw.ellipse(screen,self.color,self.rect )
        #debug - - - - -
        pygame.draw.line(screen,(255,255,255),(self.pos[0],self.pos[1]),(pipes[0].pos,pipes[0].gap_pos),1)
        # - - - - - -
    def jump(self):
        self.v = self.jump_force;
    def check_collision(self):
        #return 0 if safe return 1 if colliding with deadly object i.e; pipe, ceiling, floor
        if(self.pos[1] <= 0): # we have hit the ceiling
            return 1
        elif(self.pos[1] + self.size >= HEIGHT ): #we have hit the floor
            return 1
        elif(self.rect.colliderect(pipes[0].top_rect)):
            return 1
        elif(self.rect.colliderect(pipes[0].bot_rect)):
            return 1
        return 0


class Pipe:
    def __init__(self):
        self.speed = 2
        self.width = 80
        self.height = HEIGHT
        self.color = (20,230,20)
        self.pos = WIDTH
        self.gap_range = (125,299)
        self.gap = randint(self.gap_range[0],self.gap_range[1])
        self.gap_pos = randint(0 + self.gap,HEIGHT - self.gap)
        self.top_rect = pygame.Rect(self.pos, self.gap_pos - self.gap//2 - self.height  ,self.width,self.height)
        self.bot_rect = pygame.Rect(self.pos,self.gap_pos + self.gap//2,self.width,self.height)
    def update(self):
        self.pos -= self.speed
        self.top_rect = pygame.Rect(self.pos, self.gap_pos - self.gap//2 - self.height  ,self.width,self.height)
        self.bot_rect = pygame.Rect(self.pos,self.gap_pos + self.gap//2,self.width,self.height)
        self.render()
    def render(self):
        #top half
        pygame.draw.rect(screen,self.color, self.top_rect)
        #bot half
        pygame.draw.rect(screen,self.color, self.bot_rect)

def pipe_spawner():
    pipes.append(Pipe())

sched.add_job(pipe_spawner,'interval',seconds = spawn_time)


def update():#ran once a framepygame.draw.rect(screen,self.color, (200,,self.width,self.height)   )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                birds[0].jump();
    for bird in birds:
        bird.update()
    if(pipes[0].pos < -pipes[0].width):
        pipes.remove(pipes[0])
    for pipe in pipes:
        pipe.update()


pipes.append(Pipe())
birds.append(Bird())


while True:#runs once every frame (fps)
    screen.fill(background_color)
    update()
    pygame.display.flip()#draws
    clock.tick(fps)#tick once every fps call (miliseconds)
