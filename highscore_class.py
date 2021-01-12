from Flappyglobals import *

#Class for highscore using seperate file with data
class HighScore():

    def __init__(self):
        self.highscore = 0

    #Check for new score and change that to current highscore
    def new_score(self, score):
        if score > self.highscore:
            highscore_sound.play()
            self.highscore = score
            self.save()

    #Access and read highscore document
    def load(self):
        if (not os.path.exists("highscore.txt")):
            return
        score_file = open("highscore.txt", "r")
        try:
            self.highscore = int(score_file.read())
        finally:
            score_file.close()

    #Change highscore, overwrite old score
    def save(self):
        score_file = open("highscore.txt", "w")
        try:
            score_file.write(str(self.highscore))
        finally:
            score_file.close()
