# 기능추가
# 1. 방향키의 left, right 키 계속 누르면 블럭이 계속 이동하는 기능 추가
# 2. 블럭이 어디로 떨어질지 알려주는 고스트 블럭 추가
# 3. 연속으로 득점하면 콤보점수는 기능 추가
# 4. 아래로 블럭 내릴때 SPACE가 아니라 방향키 down으로 바꾸는 기능 추가
# 5. SPACE누르면 한번에 떨어지는 기능 추가

import sys
from math import sqrt
from random import randint
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_DOWN, K_UP, K_SPACE, K_KP_ENTER

# 게임화면 구현
pygame.init()
SURFACE = pygame.display.set_mode([600, 600])
FPSCLOCK = pygame.time.Clock()
WIDTH = 12
HEIGHT = 22
back_width = 600
back_height = 700
INTERVAL = 40
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# 배경 사진 넣기
BACKGROUND = pygame.image.load('background1.jpg')
BACKGROUND = pygame.transform.scale(BACKGROUND,(back_width, back_height))


COLORS = ((255,255,255), (255, 165, 0), (127, 255, 212), (135, 206, 235),
            (144, 238, 144), (173, 255, 47), (255, 215, 0), (255, 0, 0), (70, 130, 180))
BLOCK = None
NEXT_BLOCK = None

# 블록데이터
BLOCK_DATA = (
    (
        (0, 0, 1, \
         1, 1, 1, \
         0, 0, 0),
        (0, 1, 0, \
         0, 1, 0, \
         0, 1, 1),
        (0, 0, 0, \
         1, 1, 1, \
         1, 0, 0),
        (1, 1, 0, \
         0, 1, 0, \
         0, 1, 0),
    ), (
        (2, 0, 0, \
         2, 2, 2, \
         0, 0, 0),
        (0, 2, 2, \
         0, 2, 0, \
         0, 2, 0),
        (0, 0, 0, \
         2, 2, 2, \
         0, 0, 2),
        (0, 2, 0, \
         0, 2, 0, \
         2, 2, 0)
    ), (
        (0, 3, 0, \
         3, 3, 3, \
         0, 0, 0),
        (0, 3, 0, \
         0, 3, 3, \
         0, 3, 0),
        (0, 0, 0, \
         3, 3, 3, \
         0, 3, 0),
        (0, 3, 0, \
         3, 3, 0, \
         0, 3, 0)
    ), (
        (4, 4, 0, \
         0, 4, 4, \
         0, 0, 0),
        (0, 0, 4, \
         0, 4, 4, \
         0, 4, 0),
        (0, 0, 0, \
         4, 4, 0, \
         0, 4, 4),
        (0, 4, 0, \
         4, 4, 0, \
         4, 0, 0)
    ), (
        (0, 5, 5, \
         5, 5, 0, \
         0, 0, 0),
        (0, 5, 0, \
         0, 5, 5, \
         0, 0, 5),
        (0, 0, 0, \
         0, 5, 5, \
         5, 5, 0),
        (5, 0, 0, \
         5, 5, 0, \
         0, 5, 0)
    ), (
        (6, 6, 6, 6),
        (6, 6, 6, 6),
        (6, 6, 6, 6),
        (6, 6, 6, 6)
    ), (
        (0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0),
        (0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0, \
         0, 0, 0, 0),
        (0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0),
        (0, 0, 0, 0, \
         0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0)
    )

)

class Block:
    def __init__(self, count):
        self.turn = randint(0, 3)
        self.type = BLOCK_DATA[randint(0, 6)]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data)))
        self.xpos = randint(2, 8 - self.size)
        self.ypos = 1 - self.size
        self.fire = count + INTERVAL

    def update(self, count):
        erased, combo = 0, 0
        if is_overlapped(self.xpos, self.ypos + 1, self.turn):
            for y_offset in range(self.size):
                for x_offset in range(self.size):
                    if 0 <= self.xpos + x_offset < WIDTH and \
                            0 <= self.ypos + y_offset < HEIGHT:
                        val = self.data[y_offset * self.size + x_offset]
                        if val != 0:
                            FIELD[self.ypos + y_offset][self.xpos + x_offset] = val

            erased, combo = erase_line()
            go_next_block(count)

        if self.fire < count:
            self.fire = count + INTERVAL
            self.ypos += 1
        return erased, combo

    def draw(self):
        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if 0 <= ypos + self.ypos < HEIGHT and \
                    0 <= xpos + self.xpos < WIDTH and val != 0:
                x_pos = 25 + (xpos + self.xpos) * 25
                y_pos = 25 + (ypos + self.ypos) * 25
                pygame.draw.rect(SURFACE, COLORS[val], (x_pos, y_pos, 24, 24))



# 고스트블록 기능 추가
def draw_ghost():
    ghost_x, ghost_y = BLOCK.xpos, BLOCK.ypos
    while not is_overlapped(ghost_x, ghost_y + 1, BLOCK.turn):
        ghost_y += 1

    for index in range(len(BLOCK.data)):
        xpos = index % BLOCK.size
        ypos = index // BLOCK.size
        val = BLOCK.data[index]
        if 0 <= ypos + ghost_y < HEIGHT and \
                0 <= xpos + ghost_x < WIDTH and val != 0:
            x_pos = 25 + (xpos + ghost_x) * 25
            y_pos = 25 + (ypos + ghost_y) * 25
            pygame.draw.rect(SURFACE, (220, 220, 220), (x_pos, y_pos, 24, 24))  # Ghost block in gray

def erase_line():
    erased, combo = 0, 0
    ypos = 20
    while ypos >= 0:
        if all(FIELD[ypos]):
            erased += 1
            combo += 1
            del FIELD[ypos]
            FIELD.insert(0, [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8])
        else:
            ypos -= 1
    return erased, combo

def is_game_over():
    filled = 0
    for cell in FIELD[0]:
        if cell != 0:
            filled += 1
    return filled > 2

def go_next_block(count):
    global BLOCK, NEXT_BLOCK
    BLOCK = NEXT_BLOCK if NEXT_BLOCK != None else Block(count)
    NEXT_BLOCK = Block(count)

def is_overlapped(xpos, ypos, turn):
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if 0 <= xpos + x_offset < WIDTH and \
                    0 <= ypos + y_offset < HEIGHT:
                if data[y_offset * BLOCK.size + x_offset] != 0 and \
                        FIELD[ypos + y_offset][xpos + x_offset] != 0:
                    return True
    return False


    
def main():
    global INTERVAL
    count, score = 0, 0
    game_over = False
    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 72)
    message_over = largefont.render("GAME OVER!!", True, (0, 255, 225)) 
    # message_font = smallfont("press Enter key", True, (0, 255, 225))
    message_rect = message_over.get_rect()
    message_rect.center = (300, 300)
    go_next_block(INTERVAL)

    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 8 if xpos == 0 or xpos == WIDTH - 1 else 0
    for index in range(WIDTH):
        FIELD[HEIGHT - 1][index] = 8

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
            if count % 1000 == 0:
                INTERVAL = max(1, INTERVAL - 2)
            erased, combo = BLOCK.update(count)

            if erased > 0:
                score += (2 ** erased) * 100 * (combo if combo > 1 else 1)

            next_x, next_y, next_t = BLOCK.xpos, BLOCK.ypos, BLOCK.turn
            if key == K_UP:
                next_t = (next_t + 1) % 4
                
            # spacebar 키 누르면 한번에 내려가는 기능 추가
            elif key == K_SPACE: 
                while not is_overlapped(next_x,next_y+1,next_t):
                    next_y += 1
            # elif key == K_RIGHT:
            #     next_x += 1
            # elif key == K_LEFT:
            #     next_x -= 1
            elif key == K_DOWN:
                next_y += 1
            
            # 키 계속 누르면 해당 위치로 계속 가는 기능 추가
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                next_x -= 1
            elif keys[K_RIGHT]:
                next_x += 1

            if not is_overlapped(next_x, next_y, next_t):
                BLOCK.xpos = next_x
                BLOCK.ypos = next_y
                BLOCK.turn = next_t
                BLOCK.data = BLOCK.type[BLOCK.turn]
        
        # SURFACE.fill((0, 0, 0))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                val = FIELD[ypos][xpos]
                pygame.draw.rect(SURFACE, COLORS[val], (xpos * 25 + 25, ypos * 25 + 25, 24, 24))

        draw_ghost()
        BLOCK.draw()

        for ypos in range(NEXT_BLOCK.size):
            for xpos in range(NEXT_BLOCK.size):
                val = NEXT_BLOCK.data[xpos + ypos * NEXT_BLOCK.size]
                pygame.draw.rect(SURFACE, COLORS[val], (xpos * 25 + 460, ypos * 25 + 100, 24, 24))

        score_str = str(score).zfill(6)
        score_image = smallfont.render(score_str, True, (0, 255, 0))
        SURFACE.blit(score_image, (500, 30))

        if game_over:
            SURFACE.blit(message_over, message_rect)

        pygame.display.update()
        FPSCLOCK.tick(15)
        
        # 배경 이미지 그리기
        SURFACE.blit(BACKGROUND, (0, 0))
        
        # 화면 업데이트
        pygame.display.update()
FPSCLOCK.tick(30)
            
if __name__ == '__main__':
    main()
