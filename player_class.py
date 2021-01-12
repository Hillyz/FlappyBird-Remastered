from Flappyglobals import *

#Player sprite
class Player(pg.sprite.Sprite):
    #Initialize class
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.index = 0 #Used to change image for animation
        self.image = pg.transform.scale(player_imgs[self.index%2], (40, 40)) #Player graphic
        self.image.set_colorkey(BLACK) #Removes black square behind graphic on screen
        #Sprites are defined as rects, which makes it easy to detect collision and use coordinates
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT//3) #Player spawn point
        self.velocity = 20 #Player initial falling speed
        self.dead = True #Boolean to determine if dead or not, used to determine gamestate

    #Function for falling, based on downwards acceleration
    def gravity(self):
        g = 7
        self.velocity += g #Acceleration
        #Limits movement to stay in screen
        if self.rect.y <= deadzone:
            self.rect.y += self.velocity #Updates velocity, bird accelerates
        else:
            #Player dies
            self.dead = True


        #Movement limits top of screen
        if self.rect.y < 20:
            self.rect.y = 20


    #Player action
    #Makes the bird do its classic jump by changing the velocity to go in the opposite direction
    def jump(self):
        self.velocity = -40

    #Function that makes the bird rotate around itself based on velocity
    def bird_rotation(self):
        angle = sigma(-self.velocity*0.01) #calculates angle in degrees based on velocity
        new_image = pg.transform.scale(player_imgs[self.index%2], (40, 40))
        new_image.set_colorkey(BLACK) #Removes black square
        self.image = pg.transform.rotate(new_image, angle)#Rotates the new image


    #Collision function
    def collision(self, group2):
        collision = pg.sprite.spritecollide(self, group2, False) #Checks collision
        if collision:
            return True
