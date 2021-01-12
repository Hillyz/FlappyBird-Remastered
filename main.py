#Import globals and classes
from Flappyglobals import *
from player_class import *
from pipe_class import *
from button_class import *
from highscore_class import *


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
    final_score = 0
    score = final_score

    #Load highscore
    highscore = HighScore()
    highscore.load()


    #Nested function for help screen
    def help():

        while True:
            #Event loop
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                #Game exit
                if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
            #Return to menu screen
            if keys[pg.K_BACKSPACE]:
                return menu()


            #Draw
            SCREEN.fill(BLACK) #Clear screen
            SCREEN.blit(background, background_rect)
            players.draw(SCREEN)
            pipes.draw(SCREEN)

            #Draw help on screen
            draw_text(SCREEN, "HOW TO PLAY: ", WIDTH//2, HEIGHT//4)
            draw_text(SCREEN, "Just click the mouse", WIDTH//2, HEIGHT//3)
            draw_text(SCREEN, "To quit: ", WIDTH//2, HEIGHT//1.6)
            draw_text(SCREEN, "Press escape", WIDTH//2, HEIGHT//1.5)
            draw_text(SCREEN, "Return to menu:", WIDTH//2, HEIGHT//1.2)
            draw_text(SCREEN, "Press backspace", WIDTH//2, HEIGHT//1.1)

            #Update
            pg.display.update()

    #Nested function for menu screen
    def menu():

        #Call nonlocal variables
        nonlocal score
        nonlocal final_score

        #Menu loop
        while True:

            keys = pg.key.get_pressed()
            #Event loop
            for event in pg.event.get():
                #Game exit
                if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
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

            final_score = score
            highscore.new_score(final_score)

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

            draw_text(SCREEN, f"HIGHSCORE: {highscore.highscore}", WIDTH//2, 200)
            menusprites.draw(SCREEN)

            #Update display
            pg.display.update()


    #Nested function for play gamestate
    def play():

        #variables
        nonlocal frame_counter
        nonlocal score
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
