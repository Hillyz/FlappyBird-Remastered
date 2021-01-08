import pygame as pg

pg.init()
pg.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
clock = pg.time.Clock()
FPS = 60
WIDTH = 600
HEIGHT = 800
deadzone = 700
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("FLAPPY BIRD (REMASTERED(2020/2021 EDITION))")

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255,140,0)

#Font stuff
font_name = pg.font.match_font('arial')
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
score = 0
highscore = 0

#Load sounds
woosh_sound = pg.mixer.Sound("WOosh.wav")
score_sound = pg.mixer.Sound("pling.wav")
