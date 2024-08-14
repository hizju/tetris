"""
go_next_block() : 현재 블럭과 다음 블럭 만들기  (BLOCK, NEXT_BLOCK)
블럭을 만들었으면 BLOCK 그리기 BLOCK.draw()

키값 처리 루틴 만들기  
KEYDOWN,  K_DOWN, K_LEFT, K_RIGHT, K_SPACE

key 변수 추가 
"""

import sys
import pygame
import time
from math import sqrt
from random import randint

from pygame.constants import KEYDOWN,  K_DOWN, K_LEFT, K_RIGHT, K_UP
from data import BLOCK_DATA
from pygame.locals import QUIT

INTERVAL = 40
class Block:
    def __init__(self,count):
        self.turn = randint(0,3)
        self.type = BLOCK_DATA[randint(0,6)]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data)))
        self.xpos = randint(2,8 - self.size)
        self.ypos = 1 - self.size
        self.fire = count + INTERVAL

    def draw(self):

        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if 0 <= ypos + self.ypos < HEIGHT and \
               0 <= xpos + self.xpos < WIDTH and val != 0:
                x_pos = 25 + (xpos + self.xpos) * 25
                y_pos = 25 + (ypos + self.ypos) * 25
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (x_pos, y_pos, 24, 24))


pygame.init()
SURFACE = pygame.display.set_mode([600,600])
pygame.display.set_caption("테트리스")
FPSCLOCK = pygame.time.Clock()
WIDTH = 12
HEIGHT = 22
FIELD = [ [ 0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
COLORS = ((0, 0, 0), (255, 165, 0), (0, 0, 255), (0, 255, 255), \
          (0, 255, 0), (255, 0, 255), (255, 255, 0), (255, 0, 0), (128, 128, 128))
BLOCK = None
NEXT_BLOCK = None

def go_next_block(count):
    global BLOCK, NEXT_BLOCK
    BLOCK = NEXT_BLOCK if NEXT_BLOCK != None else Block(count)
    NEXT_BLOCK = Block(count)

def main():

    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 72)
    message_over = largefont.render("GAME TEST!!", True,(0,255,255))
    message_rect = message_over.get_rect()
    message_rect.center = (300,100)
    
    go_next_block(INTERVAL)

    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 8 if xpos == 0 or xpos == WIDTH -1 else 0

    for index in range(WIDTH):
        FIELD[HEIGHT-1][index] = 8

    while True:
        key = None
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key = event.key

        

        if key == K_DOWN:
            BLOCK.ypos += 1
        if key == K_RIGHT:
            BLOCK.xpos +=1
        if key == K_LEFT:
            BLOCK.xpos -= 1
        if key == K_UP:
            BLOCK.turn = (BLOCK.turn + 1) % 4
            
    



        SURFACE.fill((0,0,0))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                val = FIELD[ypos][xpos]
                pygame.draw.rect(SURFACE, COLORS[val],(xpos*25 +25, ypos*25 + 25, 24,24))
               


        BLOCK.draw()
    
        pygame.display.update()
        FPSCLOCK.tick(15)
        



if __name__ == '__main__':
    main()
