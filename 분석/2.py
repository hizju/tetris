"""
FPSCLOCK = pygame.time.Clock()
FPSCLOCK.tick(15)
"""

import sys
import pygame
from pygame.locals import QUIT
pygame.init()
SURFACE = pygame.display.set_mode([600,600])
pygame.display.set_caption("테트리스")
FPSCLOCK = pygame.time.Clock()



def main():
    
    while True:
        SURFACE.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(15)
        
if __name__ == '__main__':
    main()

