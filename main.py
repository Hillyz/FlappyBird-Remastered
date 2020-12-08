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
        self.pos = (HEIGHT//2)

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

    def collision(self, group2):
        collision = pg.sprite.spritecollide(self, group2, False)
        if collision:
            return True


#Pipe sprite
class Pipe(pg.sprite.Sprite):
    def __init__(self, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.h = h
        self.pos = WIDTH
        self.velocity = 0.1
        self.rect.bottomleft = (WIDTH, deadzone)

    def move(self):
        self.pos -= self.velocity
        self.rect.x = self.pos

def main():
    #local variables
    frame_counter = 0
    player = Player()
    pipes = pg.sprite.Group()
    all_sprites = pg.sprite.Group()
    all_sprites.add(player)
    pipe = Pipe(200)
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


        if player.collision(pipes):
            print("Player dead")

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
