import pygame
import random
import sys

import animationConstants
import gameConstants
import game
from agent.agent import Agent




class Experiment:

    def __init__(self):
        self.epoch = 0






# plays our awesome RenFair music
def startBgMusic():
    if PLAY_BG_MUSIC:
        randSong = random.randint(0, len(BG_MUSIC) - 1)
        pygame.mixer.music.load("../assets/music/background/" + BG_MUSIC[randSong])
        pygame.mixer.music.play(-1)


def pop():

if __name__ == "__main__":
    main()