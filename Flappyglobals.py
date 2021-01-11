#Import modules
import pygame as pg
import sys
import random
from math import *

#Initialize pygame
pg.init()
pg.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize

#Global variables
clock = pg.time.Clock()
FPS = 60
WIDTH = 600
HEIGHT = 800
deadzone = 700
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("FLAPPY BIRD (REMASTERED(2020/2021 EDITION))")

#Colours
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255,140,0)

#Font stuff
font_name = "font.ttf"
font = pg.font.Font(font_name, 44)

#Load graphics
player_imgs = []
background = pg.image.load("Background.png").convert()
background_rect = background.get_rect()
player_img1 = pg.image.load("Bird1.png").convert()
player_img2 = pg.image.load("Bird2.png").convert()
player_imgs.append(player_img1)
player_imgs.append(player_img2)
pipe_img1 = pg.image.load("Pipe_sprite.png").convert()
pipe_img2 = pg.image.load("Pipe_sprite2.png").convert()
play_button = pg.image.load("Play.png").convert()

#Load sounds
woosh_sound = pg.mixer.Sound("WOosh.wav")
score_sound = pg.mixer.Sound("pling.wav")
highscore_sound = pg.mixer.Sound("highscore.wav")
boink_sound = pg.mixer.Sound("boink.wav")
oof_sound = pg.mixer.Sound("oof.wav")

#Volume settings
woosh_sound.set_volume(0.2)
score_sound.set_volume(0.45)
highscore_sound.set_volume(1)
boink_sound.set_volume(1)
oof_sound.set_volume(1)


#Global functions
#General function to show text on screen
def draw_text(surface, text, x, y):
    text_surface = font.render(text, True, ORANGE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


#Function to calculate acceleration
#Used for falling speed and rotation of bird
def sigma(x):
    return 180 / (1 + e**(-x)) - 75
