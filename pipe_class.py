from Flappyglobals import *

#Pipe sprite
#Based on rect
class Pipe(pg.sprite.Sprite):
    #Initialize sprite
    def __init__(self, len, space):
        pg.sprite.Sprite.__init__(self)
        #Determines whether the pipe is on top or bottom of the screen
        if space == deadzone:
            self.image = pg.transform.scale(pipe_img1, (40, len))
        else:
            self.image = pg.transform.scale(pipe_img2, (40, len))

        self.image.set_colorkey(BLACK) #Removes black square
        self.rect = self.image.get_rect()
        self.len = len #Undefined length variable for random height for the pipes
        self.velocity = 5 #Speed
        self.rect.bottomleft = (WIDTH, space) #Space --> top or bot of screen

    #Function to move sprite from right to left
    def move(self):
        self.rect.x -= self.velocity
