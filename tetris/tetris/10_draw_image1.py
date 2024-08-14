"""
load(filename) -> Surface
filename : 이미지 파일

blit(source, dest, area=None, special_flags=0) -> Rect
source : 원본이 되는 Surface
dest :  복사하는 좌표(왼쪽 위)
area : 복사하는 영역(일부만 그릴때)
special_flags: 복사할 때의 연산 방법
"""

""" draw_image1.py """
import sys
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400, 300))
FPSCLOCK = pygame.time.Clock()

def main():

    logo = pygame.image.load('pythonlogo.jpg')

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((200,200,200))


        # 왼쪽 위 (20, 50) 위치에 로고를 그린다.
        SURFACE.blit(logo,(20,50))
        pygame.display.update()
        FPSCLOCK.tick(30)

if __name__ == '__main__':
    main()
