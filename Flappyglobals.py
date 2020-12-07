import pygame as pg

pg.init()
clock = pg.time.Clock()
FPS = 60
WIDTH = 600
HEIGHT = 800
deadzone = 700
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("FLAPPY BIRD (REMASTERED(2020 EDITION))")

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
