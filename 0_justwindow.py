"""justwindow.py"""
"""윈도우 표시"""

import sys
import pygame
from pygame.locals import QUIT


pygame.init()
SURFACE = pygame.display.set_mode((400,300))
pygame.display.set_caption("Just window")

def main():
    """main routine"""
    while True:
        SURFACE.fill((255,0,0))


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == '__main__':
    main()
