import pygame as pg
from pygame.locals import *
from setting import *

#バリアの形を設定
shape = [
    [0,0,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,0,0,0,0,0,0,0,1,1,1,1]
]

class Barrier(pg.sprite.Sprite):
    def __init__(self,x,y) -> None:
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((5,10))
        self.rect = self.image.get_rect(topleft= (x,y))
        self.image.fill(RED)
