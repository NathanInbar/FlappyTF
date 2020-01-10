import pygame#handles the game part (flappy bird)
import sys#handles System functions (exiting the pygame window)
from random import randint#handles random num generation in a range
from apscheduler.schedulers.background import BackgroundScheduler# scheduler is used for pipe spawning
import tensorflow as tf#handles Neural Network
#- - - - -

pygame.init()#initalizes the game

#Constants - - - -
WIDTH = 800#window width
HEIGHT = 600#window height
#4:3 aspect ratio
fps = 120#limits the game to update at max 120 times per second (after it updates, it will wait ~0.008seconds before updating again)
G = -.4#gravity
spawn_time = 1.5#seconds between pipe spawns
background_color = (43,42,42)#dark grey
#end constants - - - -

#pygame -  - - - -
screen = pygame.display.set_mode([WIDTH,HEIGHT])#sets the pygame display to have the correct dimensions
pygame.display.set_caption("Flappy Bird TF -- Justin && Nathan")#window title
clock = pygame.time.Clock()#initalizes clock object, so we start the game with the correct update delay (see fps var)
# - - - -

#pipes - - - -
sched = BackgroundScheduler()#BackgroundScheduler will handle the spawning of pipes
sched.start()#initalizes pipe spawning
# - - - -

birds = []#list that holds all the birds spawned
pipes = []#list that holds all the pipes spawned

class Bird: #class bird will define what a bird is
    def __init__(self): #called when Bird object is created
        self.pos = (100,150)#starting postition on the sreen
        self.v = 0#starting velocity
        self.size = 25#size of the bird (rendered as ellipse. size defines hitbox size which is rectangular)
        self.jump_force = 9#applied force when jump is pressed
        self.color = (200,200,5)#yellow
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size,self.size)#initalize hitbox with given parameters

    def update(self):#will run once per frame

        self.pos = (self.pos[0],self.pos[1] - self.v)  #changes position based on it's velocity.
        self.v += G #changes our velocity due to gravity 'G'

        #death - - -
        if (self.check_collision() == 1): # if bird is dead
            print('bird dead')#print dead. Eventually will signal Neural Network that this bird has died.
        # - - - -

        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size,self.size)#set its hitbox. must be set every frame
        self.render()#calls render

    def render(self):#defines how this object will be visually represented
        pygame.draw.ellipse(screen,self.color,self.rect) #draw ellipse based on hitbox
        #debug - - - - -
        pygame.draw.line(screen,(255,255,255),(self.pos[0],self.pos[1]),(pipes[0].pos,pipes[0].gap_pos),1)#draw debug line to pipe-set center of pipe-set at first index of pipes[]
        # - - - - - -

    def jump(self):#defines what happens when the bird jumps
        self.v = self.jump_force;#bird's velocity is set to force of jump

    def check_collision(self):#check if bird has died.
    #returns 0 if safe, return 1 if colliding with deadly object i.e; pipe, ceiling, floor
        if(self.pos[1] <= 0): #bird has hit the cieling
            return 1
        elif(self.pos[1] + self.size >= HEIGHT ):#bird has hit the floor
            return 1
        elif(self.rect.colliderect(pipes[0].top_rect)):#bird has hit top pipe of first pipe-set in pipes[]
            return 1
        elif(self.rect.colliderect(pipes[0].bot_rect)):#bird has hit bottom pipe of first pipe-set in pipes[]
            return 1
        return 0 #if none of the above cases happened, return safe


class Pipe:#each 'Pipe' is actually a pair of 2 pipes, one being the bottom and one being the top
    def __init__(self):#when a 'Pipe' object is created,
        self.speed = 2#as soon as its created it will start moving at rate 'speed'
        self.width = 80#width of both top and bottom pipes
        self.height = HEIGHT#height of both pipes. set to screen size so pipes will always extend far enough to go off-screen no matter the position
        self.color = (20,230,20)#green
        self.pos = WIDTH#start position of the pipes is on the right end of the screen
        self.gap_range = (125,299)#gap between the 2 pipes can be between these two
        self.gap = randint(self.gap_range[0],self.gap_range[1])#picks random number in gap_range
        self.gap_pos = randint(0 + self.gap,HEIGHT - self.gap)#gap_pos can range from high on the to low on the screen while making sure both pipes will at least be visible
        self.top_rect = pygame.Rect(self.pos, self.gap_pos - self.gap//2 - self.height  ,self.width,self.height)#set its hitbox.
        self.bot_rect = pygame.Rect(self.pos,self.gap_pos + self.gap//2,self.width,self.height)#set its hitbox.
    def update(self):#called every frame
        self.pos -= self.speed#move the pipe set by predefined speed
        self.top_rect = pygame.Rect(self.pos, self.gap_pos - self.gap//2 - self.height  ,self.width,self.height)#set its hitbox. must be set every frame to make sure its in the latest updated position
        self.bot_rect = pygame.Rect(self.pos,self.gap_pos + self.gap//2,self.width,self.height)#set its hitbox. must be set every frame to make sure its in the latest updated position
        self.render()#draw the pipe set onto the screen

    def render(self):#defines how this object will be visually represented
        pygame.draw.rect(screen,self.color, self.top_rect)#draws top pipe's rectangle from hitbox
        pygame.draw.rect(screen,self.color, self.bot_rect)#draws bottom pipe's rectangle from hitbox

def pipe_spawner():#method that will be continuously called by a BackgroundScheduler
    pipes.append(Pipe())#when called, add another pipe-set into the game

sched.add_job(pipe_spawner,'interval',seconds = spawn_time)#tells scheduler to run pipe_spawner() every 'spawn_time' seconds


def update():#ran once a frame
#Pygame events- - - - - - - - - -
    for event in pygame.event.get():#for every event we told pygame to preform between updates (excluding draw requests),
        if event.type == pygame.QUIT:#quit game if that is a called event
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:#if any key is pressed,
            if event.key == pygame.K_SPACE:#and that key is space,
                birds[0].jump();#make first bird in list jump if user pressed space -- !! MUST BE DEPRECATED ONCE NEURAL NETWORK HANDLES BIRDS!!
# - - - - - - - - - - - - - - - -
#Bird/Bird's- - - - - - - - - - -
    for bird in birds:#for every bird,
        bird.update()#tell all birds to call their update function
# - - - - - - - - - - - - - - - -
#Pipe/Pipe's- - - - - - - - - - -
    if(pipes[0].pos < -pipes[0].width):#if oldest pipe-set position is less than the opposite of it's width,
    # (ex: oldest pipe position=-81 (completely off screen),  negative pipe width=-80 then-> True)
        pipes.remove(pipes[0])#delete the pipe object

    for pipe in pipes:#for every pipe,
        pipe.update()#tell all pipes to call their update function
# - - - - - - - - - - - - - - - -


pipes.append(Pipe())#start game with 1 pipe-set
birds.append(Bird())#start game with 1 bird


while True:#pauses between iterations by the delay (in ms). where the delay is fps/1000. (convert frames per SECOND to frames per MS)
    screen.fill(background_color)#draw background
    update()#call main update function
    pygame.display.flip()#takes all the draw requests and updates the screen
    clock.tick(fps)#tick once every fps call (fps converted to miliseconds)
#-- end main.py --
