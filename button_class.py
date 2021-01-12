from Flappyglobals import *

#Sprite for the button that shows up in the menu
#Could perhaps simply be an image, but I thought of this first so here it is
class Menubutton(pg.sprite.Sprite):

    def __init__(self, img, h):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, h)
