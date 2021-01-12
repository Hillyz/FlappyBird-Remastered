#Import globals
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


#Sprite for the button that shows up in the menu
#Could perhaps simply be an image, but I thought of this first so here it is
class Menubutton(pg.sprite.Sprite):
    def __init__(self, img, h):
        pg.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, h)


#Main function where everything is executed
def main():

    #Initialize sprites and add to group
    playbutton = Menubutton(play_button, HEIGHT//2) #Initializes object
    helpbutton = Menubutton(help_button, HEIGHT//1.2)
    menusprites = pg.sprite.Group() #Group for sprites in the menu
    menusprites.add(playbutton)
    menusprites.add(helpbutton)
    pipes = pg.sprite.Group()
    players = pg.sprite.Group()
    player = Player()
    pipe1 = Pipe(200, deadzone) #Lower pipe
    pipe2 = Pipe(HEIGHT-250, 250) #Higher pipe
    pipes.add(pipe1, pipe2)

    #Local variables
    frame_counter = 0
    pipe_diff = 250 #Constant for the room between a pair of pipes
    score = 0
    init_highscore = 0
    highscore = init_highscore


    def help():
        while True:
            #Event loop
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                #Game exit
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            if keys[pg.K_BACKSPACE]:
                return menu()


            #Draw
            SCREEN.fill(BLACK) #Clear screen
            SCREEN.blit(background, background_rect)
            players.draw(SCREEN)
            pipes.draw(SCREEN)
            draw_text(SCREEN, "HOW TO PLAY: ", WIDTH//2, HEIGHT//3)
            draw_text(SCREEN, "Just click the mouse", WIDTH//2, HEIGHT//2)
            draw_text(SCREEN, "To return to menu", WIDTH//2, HEIGHT//1.2)
            draw_text(SCREEN, "Press backspace", WIDTH//2, HEIGHT//1.1)


            #Update
            pg.display.update()

    #Nested function for menu screen
    def menu():
        #Call nonlocal variables
        nonlocal highscore
        nonlocal init_highscore
        nonlocal score

        #Menu loop
        while True:
            #Event loop
            for event in pg.event.get():
                #Game exit
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                #Check if mouse is clicked
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                     pos = pg.mouse.get_pos()

                     #Check if mouse is on the button when clicked
                     if playbutton.rect.collidepoint(pos):
                         player.dead = False
                         #Ends menu gamestate, playing starts
                         return play()

                     if helpbutton.rect.collidepoint(pos):
                        return help()

            #Checks if there is a new high score
            if highscore > init_highscore:
                init_highscore = highscore
                highscore_sound.play()

            #Draws everything on screen
            SCREEN.fill(BLACK) #Clear screen
            SCREEN.blit(background, background_rect)
            players.draw(SCREEN)
            pipes.draw(SCREEN)

            #Draws score on screen
            #If statements to get around bug, quick fix
            if score >= 0:
                draw_text(SCREEN, f"SCORE: {score}", WIDTH//2, 50)
            else:
                score = 0

            draw_text(SCREEN, f"HIGHSCORE: {highscore}", WIDTH//2, 200)
            menusprites.draw(SCREEN)

            #Update display
            pg.display.update()


    #Nested function for play gamestate
    def play():
        #variables
        nonlocal frame_counter
        nonlocal score
        nonlocal highscore
        score = -1 #Begins at -1 instead of 0 to make the algorithm to count score easier

        #Clear sprite groups to reset screen
        pipes.empty()
        players.empty()
        #Initialize player object and add to sprite group
        player = Player()
        players.add(player)

        #Game loop
        while True:
            #Run game at set speed
            clock.tick(FPS)
            frame_counter += 1

            #Every 6 frames, animation updates to simulate wing flapping
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
                if player.collision(pipes):
                    boink_sound.play()
                else:
                    oof_sound.play()

                player.dead = True
                #Changes gamestate from playing to menu
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

                #Timing of passing a pipe and spawning a new one is equal
                #Therefore the score increases simply every time a pipe is spawned
                #However because of this, score has to start at -1 because of the first pipe that spawns
                score += 1
                #If to quick fix score starting at -1
                if score > 0:
                    score_sound.play()
                #Checks if a current score is the highest so far
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
            #If to quick fix score starting at -1
            if score >= 0:
                draw_text(SCREEN, str(score), WIDTH//2, 50)

            #Update display
            pg.display.update()

    #Call menu to start the program from the menu
    menu()

#Run the thing
main()
