import pygame
from pygame.locals import *
import sys

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('example')

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
pygame.quit()
sys.exit()