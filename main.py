from Flappyglobals import *
import sys

#Player sprite
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.velocity = 0.5
        #Positional variable to calculate float value for y-coordinate
        self.pos = (HEIGHT//2)

    def gravity(self):
        #Caps speed
        if self.velocity < 0.75:
            self.velocity += 0.015 #Acceleration
        #Limits movement to stay in screen
        if self.rect.y <= deadzone - 20 and self.pos <= deadzone-20:
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
        self.velocity = -2

    #Collision function
    def collision(self, group2):
        collision = pg.sprite.spritecollide(self, group2, False)
        if collision:
            return True


#Pipe sprite
class Pipe(pg.sprite.Sprite):
    def __init__(self, h, space):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.h = h
        self.pos = WIDTH
        self.velocity = 0.1
        self.rect.bottomleft = (WIDTH, space) #Space --> top or bot of screen

    def move(self):
        self.pos -= self.velocity
        self.rect.x = self.pos

def main():
    #local variables
    frame_counter = 0
    player = Player()
    pipes = pg.sprite.Group()
    players = pg.sprite.Group()
    players.add(player)
    pipe1 = Pipe(200, deadzone) #Lower pipe
    pipe2 = Pipe(HEIGHT-250, 250) #Higher pipe
    pipes.add(pipe1, pipe2)
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
            print("Player dead")

        #Pipe movement and spawning
        for pipe in pipes:
            pipe.move()
            if pipe.rect.x < 0:
                pipe.remove(pipes)
            if frame_counter % 4000 == 0:
                pipe1 = Pipe(200, deadzone)
                pipe2 = Pipe(HEIGHT-250, 250)
                pipes.add(pipe1, pipe2)

        #Update
        players.update()
        pipes.update()

        #draw
        SCREEN.fill(BLACK)
        players.draw(SCREEN)
        pipes.draw(SCREEN)

        #Update display
        pg.display.update()

main()
