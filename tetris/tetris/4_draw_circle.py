"""
circle(Surface, color, pos, radius, width=0) -> Rect
Surface : 그리는 대상이 되는 화면(Surface 객체)
color : 색
pos : 중심좌표
radius: 반경
width : 선 폭(생략 시는 꽉 채워 칠한다.)
"""


""" draw_circle.py """
import sys
import pygame
from pygame.locals import QUIT, Rect

pygame.init()
SURFACE = pygame.display.set_mode((400,300))
FPSCLOCK = pygame.time.Clock()

def main():

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((255, 255, 255))

        #빨간색: 꽉 채워 칠한다.
        pygame.draw.circle(SURFACE, (255, 0, 0), (50, 50), 20)

        #빨간색: 굵기 10
        pygame.draw.circle(SURFACE, (255, 0, 0), (150, 50), 20, 10)

        #녹색: 반경 10
        pygame.draw.circle(SURFACE, (0, 255, 0), (50, 150), 10)

        #녹색: 반경 20
        pygame.draw.circle(SURFACE, (0, 255, 0), (150, 150), 20)

        #녹색: 반경 30
        pygame.draw.circle(SURFACE, (0, 255, 0), (250, 150), 30)

        pygame.display.update()
        FPSCLOCK.tick(3)

if __name__ == '__main__':
    main()
        

        


                
