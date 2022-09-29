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

#バリア生成用のメソッドを作成
def create_barrier(barrierSprite):
    #4つ配置するので、range(4)
    for ind in range(4):
        for i, row in enumerate(shape):
            for j, col in enumerate(row):
                if col == 1:
                    barrier = Barrier(j*5+32+(ind*(WIDTH // 4)),i*10+(HEIGHT-120))
                    barrierSprite.add(barrier)
    return barrier,barrierSprite