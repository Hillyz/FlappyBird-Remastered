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
        self.pos = (WIDTH//2)

    def gravity(self):
        if self.velocity < 0.5:
            self.velocity += 0.05
        if self.rect.y <= deadzone - 20 and self.pos <= deadzone-20:
            self.pos += self.velocity
            self.rect.y = int(self.pos)
        else:
            self.rect.y = deadzone - 20
            self.pos = deadzone - 20

        if self.rect.y < 20 and self.pos < 20:
            self.rect.y = 20
            self.pos = 20

    def jump(self):
        self.velocity = -4


#Pipe sprite
class Pipe(pg.sprite.Sprite):
    def __init__(self, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, 100))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.y = y
        self.rect.topleft = (WIDTH, self.y)

    def move(self):
        self.rect.x += 10

def main():
    #local variables
    frame_counter = 0
    player = Player()
    pipes = pg.sprite.Group()
    all_sprites = pg.sprite.Group()
    all_sprites.add(player)
    pipe = Pipe(400)
    pipes.add(pipe)
    # Game loop
    while True:
        #Run game at set speed
        clock.tick()
        frame_counter += 1

        #game exit
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONUP:
                player.jump()

        #Player movement
        if frame_counter % 3 == 0:
            player.gravity()



        for pipe in pipes:
            pipe.move()

        #Update
        all_sprites.update()
        pipes.update()

        #draw
        SCREEN.fill(BLACK)
        all_sprites.draw(SCREEN)
        pipes.draw(SCREEN)

        #Update display
        pg.display.update()

main()
