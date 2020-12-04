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

    def gravity(self):
        self.rect.y +=1 


    def jump(self):
        self.rect.y -= 60




#Pipe sprite
class Pipe(pg.sprite.Sprite):
    pass

def main():
    #local variables
    player = Player()
    all_sprites = pg.sprite.Group()
    all_sprites.add(player)
    # Game loop
    while True:
        #game exit
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP:
                player.jump()

        #Player movement
        player.gravity()


        #Update
        all_sprites.update()

        #draw
        SCREEN.fill(BLACK)
        all_sprites.draw(SCREEN)

        #Update display
        pg.display.update()

main()
