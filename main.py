from Flappyglobals import *
import sys
import random

#Player sprite
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (40, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.velocity = 0.5
        #Positional variable to calculate float value for y-coordinate
        self.pos = (HEIGHT//2)

    def gravity(self):
        g = 0.007
        self.velocity += g #Acceleration
        #Limits movement to stay in screen
        if self.rect.y <= deadzone - 20:
            self.pos += self.velocity #Updates float value
            self.rect.y = int(self.pos) #Updates rect value as int
        else:
            #Movement limits
            self.rect.y = deadzone - 20
            self.pos = deadzone - 20
        #Movement limits top of screen
        if self.rect.y < 20 and self.pos < 20:
            self.rect.y = 20
            self.pos = 20

    #Player action
    def jump(self):
        self.velocity = -1.4

    #Collision function
    def collision(self, group2):
        collision = pg.sprite.spritecollide(self, group2, False)
        if collision:
            return True


#Pipe sprite
class Pipe(pg.sprite.Sprite):
    def __init__(self, h, space):
        pg.sprite.Sprite.__init__(self)
        if space == deadzone:
            self.image = pg.transform.scale(pipe_img1, (40, h))
        else:
            self.image = pg.transform.scale(pipe_img2, (40, h))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.h = h
        #Positional x value for float
        self.pos = WIDTH

        self.velocity = 0.1
        self.rect.bottomleft = (WIDTH, space) #Space --> top or bot of screen

    def move(self):
        self.pos -= self.velocity
        self.rect.x = self.pos

def main():
    #Load graphics
    #background = pg.image.load("Background.png").convert()
    #background_rect = background.get_rect()
    #player_img = pg.image.load("Bird1.png").convert()
    #pipe_img = pg.image.load("Pipe_sprite.png").convert()

    #local variables
    frame_counter = 0
    player = Player()
    pipes = pg.sprite.Group()
    players = pg.sprite.Group()
    players.add(player)
    pipe1 = Pipe(200, deadzone) #Lower pipe
    pipe2 = Pipe(HEIGHT-250, 250) #Higher pipe
    pipes.add(pipe1, pipe2)
    pipe_diff = 300

    # Game loop
    while True:
        #Run game at set speed
        clock.tick()
        frame_counter += 1

        #Events
        for event in pg.event.get():
            #Game exit
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit()
            #Player actions
            elif event.type == pg.MOUSEBUTTONUP:
                player.jump()

        #Player natural movement
        if frame_counter % 3 == 0:
            player.gravity()

        #Check for collisions
        if player.collision(pipes):
            pass
            #print("Player dead")

        #Pipe movement
        for pipe in pipes:
            pipe.move()
            if pipe.rect.x < 0:
                pipe.remove(pipes)

        #Spawn pipes
        if frame_counter % 4000 == 0:
            pipe_len = random.randint(120, 330) #Random length of pipe
            pipe1 = Pipe(pipe_len, deadzone) #Random bot pipe
            pipe2 = Pipe(HEIGHT-pipe_len-pipe_diff, HEIGHT-pipe_len-pipe_diff) #Random top pipe
            pipes.add(pipe1, pipe2)

        #Update
        players.update()
        pipes.update()

        #draw
        SCREEN.fill(BLACK)
        SCREEN.blit(background, background_rect)
        players.draw(SCREEN)
        pipes.draw(SCREEN)

        #Update display
        pg.display.update()

main()
