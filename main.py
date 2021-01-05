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
        self.rect.center = (WIDTH//2, HEIGHT//4)
        self.velocity = 0.5
        #Positional variable to calculate float value for y-coordinate
        self.pos = (HEIGHT//4)

    def gravity(self):
        g = 0.007
        self.velocity += g #Acceleration
        #Limits movement to stay in screen
        if self.rect.y <= deadzone - 20:
            self.pos += self.velocity #Updates float value
            self.rect.y = int(self.pos) #Updates rect value as int
        else:
            #Player dies
            gamestate = "menu"
            #print(f"highscore: {highscore}")
            main()

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

class Playbutton(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = play_button
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT//2)


def draw_text(surface, text, x, y):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topright = (x, y)
    surface.blit(text_surface, text_rect)

def main():
    #local variables
    frame_counter = 0
    player = Player()
    playbutton = Playbutton()
    menusprites = pg.sprite.Group()
    pipes = pg.sprite.Group()
    players = pg.sprite.Group()
    players.add(player)
    menusprites.add(playbutton)
    pipe1 = Pipe(200, deadzone) #Lower pipe
    pipe2 = Pipe(HEIGHT-250, 250) #Higher pipe
    pipes.add(pipe1, pipe2)
    pipe_diff = 280 #Constant for the room between a pair of pipes
    score = 0
    score_delay = 0
    gamestate = "menu" #Player state

    #Menu loop
    while gamestate == "menu":
        #Events
        for event in pg.event.get():
            #Game exit
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                 pos = pg.mouse.get_pos()
                 if playbutton.rect.collidepoint(pos):
                     gamestate = "play"


        #draw
        SCREEN.fill(BLACK)
        SCREEN.blit(background, background_rect)
        menusprites.draw(SCREEN)
        players.draw(SCREEN)
        pipes.draw(SCREEN)
        draw_text(SCREEN, str(score), 50, 15)

        #Update display
        pg.display.update()

    # Game loop
    while gamestate == "play":
        #Run game at set speed
        clock.tick()
        frame_counter += 1
        score_delay += 1

        #Events
        for event in pg.event.get():
            #Game exit
            if event.type == pg.QUIT:
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
            gamestate = "menu"
            return main()


        #Pipe movement
        for pipe in pipes:
            pipe.move()
            if pipe.rect.x < 0:
                pipe.remove(pipes)

        if pipe.rect.x == player.rect.x and score_delay >= 0:
            score +=1
            score_delay = -20

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
        draw_text(SCREEN, str(score), 50, 15)

        #Update display
        pg.display.update()



main()
