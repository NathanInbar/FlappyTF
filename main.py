import pygame
import sys , time , os
import math
import random
import numpy as np

pygame.init()
#Constants
WIDTH = 800
HEIGHT = 600
#4:3 aspect ratio
fps = 60
background_color = (43,42,42)#dark grey
#end constants

screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Flappy Bird TF -- Justin && Nathan")
clock = pygame.time.Clock()


def update():#ran once a frame
    pygame.draw.ellipse(screen,(225,30,25),[25,25,25,25])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pass



while True:#runs once every frame (fps)
    screen.fill(background_color)
    update()
    pygame.display.flip()#draws
    clock.tick(fps)#tick once every fps call (miliseconds)
