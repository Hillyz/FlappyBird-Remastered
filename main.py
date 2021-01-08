from Flappyglobals import *
import sys
import random
from math import *

def sigma(x):
    return 180 / (1 + e**(-x)) - 75


#Player sprite
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.index = 0
        self.image = pg.transform.scale(player_imgs[self.index%2], (40, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT//3)
        self.velocity = 20
        #Positional variable to calculate float value for y-coordinate
        self.pos = (HEIGHT//4)
        self.dead = True #bruk til main function ting

    def gravity(self):
        g = 7
        self.velocity += g #Acceleration
        #Limits movement to stay in screen
        if self.rect.y <= deadzone:
            self.pos += self.velocity #Updates float value
            self.rect.y = int(self.pos) #Updates rect value as int
        else:
            #Player dies
            self.dead = True


        #Movement limits top of screen
        if self.rect.y < 20 and self.pos < 20:
            self.rect.y = 20
            self.pos = 20

    #Player action
    def jump(self):
        self.velocity = -40

    def bird_rotation(self):
        angle = sigma(-self.velocity*0.01)
        new_image = pg.transform.scale(player_imgs[self.index%2], (40, 40))
        new_image.set_colorkey(BLACK)
        self.image = pg.transform.rotate(new_image, angle)


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

        self.velocity = 5
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
    text_surface = font.render(text, True, ORANGE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def main():
    #local variables
    frame_counter = 0
    playbutton = Playbutton()
    menusprites = pg.sprite.Group()
    menusprites.add(playbutton)
    pipe_diff = 280 #Constant for the room between a pair of pipes
    score = 0
    highscore = 0
    pipes = pg.sprite.Group()
    players = pg.sprite.Group()
    player = Player()
    pipe1 = Pipe(200, deadzone) #Lower pipe
    pipe2 = Pipe(HEIGHT-250, 250) #Higher pipe
    pipes.add(pipe1, pipe2)
    #players.add(player)

    def menu():
        nonlocal highscore
        nonlocal score
        while True:
            for event in pg.event.get():
                #Game exit
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                     pos = pg.mouse.get_pos()
                     if playbutton.rect.collidepoint(pos):
                         player.dead = False
                         return play()


            #draw
            SCREEN.fill(BLACK)
            SCREEN.blit(background, background_rect)
            players.draw(SCREEN)
            pipes.draw(SCREEN)
            if score >= 0:
                draw_text(SCREEN, f"SCORE: {score}", WIDTH//2, 50)
            else:
                score = 0
            draw_text(SCREEN, f"HIGHSCORE: {highscore}", WIDTH//2, 200)
            menusprites.draw(SCREEN)

            #Update display
            pg.display.update()
            #bruk functions i stedet for loops og gamestate


    def play():
        nonlocal frame_counter
        nonlocal score
        score = -1
        nonlocal highscore
        pipes.empty()
        players.empty()
        player = Player()
        players.add(player)

        while True:
            #Run game at set speed
            clock.tick(FPS)
            frame_counter += 1
            if frame_counter % 6 == 0:
                player.index += 1

            #Events
            for event in pg.event.get():
                #Game exit
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                #Player actions
                elif event.type == pg.MOUSEBUTTONUP:
                    player.jump()
                    woosh_sound.play()

            #Player natural movement
            if frame_counter % 3 == 0:
                player.gravity()
                player.bird_rotation()

            #Check for collisions
            if player.collision(pipes) or player.rect.y >= deadzone:
                player.dead = True
                return menu()


            #Pipe movement
            for pipe in pipes:
                pipe.move()
                if pipe.rect.x < 0:
                    pipe.remove(pipes)


            #Spawn pipes
            if frame_counter % 60 == 0:
                pipe_len = random.randint(120, 330) #Random length of pipe
                pipe1 = Pipe(pipe_len, deadzone) #Random bot pipe
                pipe2 = Pipe(HEIGHT-pipe_len-pipe_diff, HEIGHT-pipe_len-pipe_diff) #Random top pipe
                pipes.add(pipe1, pipe2)
                score += 1
                if score > 0:
                    score_sound.play()
                if score > highscore:
                    highscore = score


            #Update
            players.update()
            pipes.update()

            #draw
            SCREEN.fill(BLACK)
            SCREEN.blit(background, background_rect)
            players.draw(SCREEN)
            pipes.draw(SCREEN)
            if score >= 0:
                draw_text(SCREEN, str(score), WIDTH//2, 50)

            #Update display
            pg.display.update()

    if player.dead == True:
        menu()
    else:
        play()


main()
