

"""
시간이 지나면 자동으로 블럭이 내려오도록 하자 : count 값 이용
게임 오버 루틴을 만들자 
is_game_over()
"""

import sys
import pygame
import time
from math import sqrt
from random import randint

from pygame.constants import KEYDOWN,  K_DOWN, K_LEFT, K_RIGHT, K_UP, K_SPACE
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
    def update(self,count):
        
        erased = 0
        if is_overlapped(self.xpos, self.ypos + 1, self.turn):
            for y_offset in range(BLOCK.size):
                for x_offset in range(BLOCK.size):
                    if 0 <= self.xpos+x_offset < WIDTH and \
                        0 <= self.ypos+y_offset < HEIGHT:
                        val = BLOCK.data[y_offset*BLOCK.size \
                                            + x_offset]
                        if val != 0:
                            FIELD[self.ypos+y_offset]\
                                 [self.xpos+x_offset] = val

            erased = erase_line()
            go_next_block(count)

        if self.fire < count:
            self.fire = count + INTERVAL
            self.ypos += 1
        

def is_game_over():
    filled = 0
    for cell in FIELD[0]:
        if cell != 0:
            filled += 1
    return filled > 2


def erase_line():
    erased = 0
    ypos = 20
    while ypos >= 0:
        if all(FIELD[ypos]):
            erased += 1
            del FIELD[ypos]
            FIELD.insert(0, [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8])
        else:
            ypos -= 1
    return erased

def is_overlapped(xpos, ypos,turn):
    global BLOCK
    data = BLOCK.type[turn]

    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if 0 <= xpos+x_offset < WIDTH and 0 <= ypos+y_offset < HEIGHT:
                if data[y_offset*BLOCK.size + x_offset] != 0 and FIELD [ypos+y_offset][xpos + x_offset] != 0:
                    return True
    return False



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

    count = 0
    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 72)
    message_over = largefont.render("GAME OVER", True,(0,255,255))
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

        game_over = is_game_over()

        if not game_over:

            count += 5

            BLOCK.update(count)

            # 블럭을 옮기기전에 벽과 충돌여부를 알아야 하기때문에 임시 변수를 만들자
            next_x, next_y, next_t = BLOCK.xpos,BLOCK.ypos, BLOCK.turn
            if key == K_DOWN:
                next_y += 1
            if key == K_RIGHT:
                next_x +=1
            if key == K_LEFT:
                next_x -= 1
            if key == K_UP:
                next_t = (next_t + 1) % 4
                
            keys = pygame.key.get_pressed() # 지속적으로 누를 때
            if keys[K_SPACE]: # 키값은 스페이스바로
                next_y += 1 # key down
                    
            
            if not is_overlapped(next_x, next_y, next_t):
                BLOCK.xpos = next_x
                BLOCK.ypos = next_y
                BLOCK.turn = next_t
                BLOCK.data = BLOCK.type[BLOCK.turn]

    
      


        SURFACE.fill((0,0,0))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                val = FIELD[ypos][xpos]
                pygame.draw.rect(SURFACE, COLORS[val],(xpos*25 +25, ypos*25 + 25, 24,24))
               


        BLOCK.draw()



        # NEXT_BLOCK 출력
        for ypos in range(NEXT_BLOCK.size):
            for xpos in range(NEXT_BLOCK.size):
                val = NEXT_BLOCK.data[xpos + ypos*NEXT_BLOCK.size]
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (xpos*25 + 460, ypos*25 + 100, 24, 24))

    
        if game_over:
            SURFACE.blit(message_over,message_rect)
        pygame.display.update()
        FPSCLOCK.tick(15)
        



if __name__ == '__main__':
    main()
