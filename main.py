# IMPORTS
import pygame
import neat
import random
import time
import os

# Window dimensions
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

'''
BIRD_IMGS = [ pygame.transform.scale2x(pygame.image.load(os.path.join('Assets', 'bird1.png') ) ), 
pygame.transform.scale2x(pygame.image.load(os.path.join('Assets', 'bird2.png') ) ), 
pygame.transform.scale2x(pygame.image.load(os.path.join('Assets', 'bird3.png') ) )]
'''

def LoadImage(file_name: str, doubled:bool = True):
    if doubled:
        return pygame.transform.scale2x(pygame.image.load(os.path.join('Assets', file_name)))
    else:
        return pygame.image.load(os.path.join('Assets', file_name))

BIRD_IMGS = [ LoadImage('bird1.png'), LoadImage('bird2.png'), LoadImage('bird3.png')]
PIPE_IMG = LoadImage('pipe.png')
BASE_IMG = LoadImage('base.png')
BG_IMG = LoadImage('bg.png')

class Bird:
    ### CONSTANTS FOR ALL AGENTS
    # Animation frames of bird
    IMGS = BIRD_IMGS
    # Tilt range of bird
    MAX_ROTATION = 25
    # Tilt speed of bird
    ROT_VEL = 20
    # Flapping speed of bird
    ANIMATION_TIME = 5

    def __init__(self, pos_horizontal, pos_vertical):
        ### AGENT PROPETIES
        # Position of agent
        self.pos_horizontal = pos_horizontal
        self.pos_vertical = pos_vertical
        # Tilt of agent
        self.tilt = 0
        # Animation tick counter
        self.tick_count = 0
        # ???
        self.vel = 0
        # Current height of jump
        self.height = 0
        # How many times the frame has been shown
        self.img_count = 0
        # Current animation frame
        self.img = self.IMGS[0]

    def Jump(self):
        # Set initial velocity of jump
        self.vel = -10.5
        # Reset tick of animation
        self.tick_count = 0
        # Reset height to current bird position
        self.height = self.pos_vertical

    def Move(self):
        # Increment tick
        self.tick_count += 1
        # Jump physics
        displacement  = self.vel*self.tick_count + 1.5*self.tick_count**2

        # Limit falling speed
        if displacement >= 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        # Apply the displacement
        self.pos_vertical += displacement

        # If we are going upwards
        if displacement < 0 or self.pos_vertical < self.height + 50:
            # Rotate the agent to the most upward rotation
            # !!! I think this 'if' might be deletable.
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        # Else we must be going downwards
        else:
            # Rotate the agent downwards until we hit the straight down
            if self.tilt > -90: # add STRAIGHT_DOWN ?
                self.tilt -= self.ROT_VEL

    def Draw(self, win):
        self.img_count += 1
        
        # Not efficient but works
        # Goddamn it feels horrible
        # Pls change it in the future
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*5:
            self.img = self.IMGS[0]
            self.img_count = 0

        # If falling down
        if self.tilt <= -80:
            # Make animation fly upwards when agent finally flaps
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # Found on stackoverflow. How does it work?
        # Rotate the agent image arount it's center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.pos_horizontal, self.pos_vertical)).center)
        # Blit the rotated image onto the screen
        win.blit(rotated_image, new_rect.topleft)

    def GetMask(self):
        return pygame.mask.from_surface(self.img)

def DrawWindow(win, bird):
    win.blit(BG_IMG, (0,0))
    bird.Draw(win)
    pygame.display.update()

def Main():
    a1 = Bird(200, 200)
    win = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()

    run = True
    
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #if event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_w:
            #        a1.Jump()
        a1.Move()
        DrawWindow(win, a1)

    pygame.quit()
    quit()

Main()



