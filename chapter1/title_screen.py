import pygame as pg
from pygame.locals import *
from setting import *

class Title():
    SCREEN.fill(BLACK)
    pg.font.init()
    draw_text(f'Invader', 60, WIDTH // 2, int(HEIGHT * 0.20), YELLOW)  
    draw_text(f'press [ S ] start', 60, WIDTH // 2, int(HEIGHT * 0.35), YELLOW)  
    draw_text(f'[space] = shot', 60, WIDTH // 2, int(HEIGHT * 0.50), WHITE)  
    draw_text(f'[arrow_right] = move', 60, WIDTH // 2, int(HEIGHT * 0.65), WHITE)  
    draw_text(f'[arrow_left]  = move', 60, WIDTH // 2, int(HEIGHT * 0.80), WHITE)  
