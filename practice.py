import os
os.environ['SDL_AUDIODRIVER'] = 'alsa'
os.environ['AUDIODEV'] = 'hw:2,0'

import pygame
import time

pygame.mixer.init()
pygame.mixer.music.load("Hot_Coffee.mp3")
#pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play()
time.sleep(10)