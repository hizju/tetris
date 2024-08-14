"""
FPSCLOCK = pygame.time.Clock()
FPSCLOCK.tick(15)

글씨 출력 추가
시간 추가 
"""

import sys
import pygame
import time
from pygame.locals import QUIT
pygame.init()
SURFACE = pygame.display.set_mode([600,600])
pygame.display.set_caption("테트리스")
FPSCLOCK = pygame.time.Clock()



def main():

    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 72)
    message_over = largefont.render("GAME TEST!!", True,(0,255,255))
    message_rect = message_over.get_rect()
    message_rect.center = (300,100)
    
    while True:
        SURFACE.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        now = time.localtime()
        str = '{0:04d}/{1:02d}/{2:02d}  {3:02d}:{4:02d}:{5:02d}'.format(now.tm_year,now.tm_mon,now.tm_mday,now.tm_hour,now.tm_min,now.tm_sec)
        SURFACE.blit(message_over,message_rect)
        watch = smallfont.render(str,True,(0,255,0))
        SURFACE.blit(watch,(300,200))
        pygame.display.update()
        FPSCLOCK.tick(15)
        



if __name__ == '__main__':
    main()

