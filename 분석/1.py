import sys
import pygame
from pygame.locals import QUIT
pygame.init()
SURFACE = pygame.display.set_mode([600,600])
pygame.display.set_caption("테트리스")


def main():
    
    while True:
        SURFACE.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()



if __name__ == '__main__':
    main()

