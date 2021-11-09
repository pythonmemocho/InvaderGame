import pygame as pg

pg.display.set_caption('Invader')

CLOCK = pg.time.Clock()
FPS = 30
WIDTH = 500
HEIGHT = 500
SCREEN = pg.display.set_mode((WIDTH,HEIGHT))

#色の設定
PLAYER_COLOR = (13,180,214)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200,0,0)
GREEN = (0,200,0)
BLUE = (0,0,200)
YELLOW = (200,200,0)
BULLET_COLOR = (0,200,200)
COLORS = [RED,GREEN,BLUE,YELLOW]

# テキスト描画用の関数
def draw_text(text, size, x, y, color):
		font = pg.font.Font(None, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		SCREEN.blit(text_surface,text_rect)

