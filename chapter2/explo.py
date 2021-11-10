import pygame as pg
from pygame.locals import *
from setting import *

class Explosion(pg.sprite.Sprite):
    def __init__(self,pos):
        pg.sprite.Sprite.__init__(self)
        
        #画像の設定
        self.explo_imgs = []
        data = pg.image.load('chapter2\images\explosion.png').convert_alpha()
        #リストに格納
        for col in range(4):
            for row in range(4):
                #スプライトシートから位置、サイズを指定してリストに格納
                img = data.subsurface((32 * row, 32 * col, 32, 32))
                img = pg.transform.scale(img,(72, 72))
                self.explo_imgs.append(img) 

        #描画する画像を指定するための設定 
        self.index = 0
        self.image = self.explo_imgs[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (pos)
        self.radius = int(75 / 2)
        #実行処理時の時間を記録
        self.last_update = pg.time.get_ticks()
        self.speed = 25
        
    #毎フレームの処理用メソッド
    def update(self):
        #実行処理時の時間を記録
        now = pg.time.get_ticks()
        if now - self.last_update > self.speed:
            self.last_update = now
            self.index += 1
            if self.index == len(self.explo_imgs):
                self.kill()
            else:
                self.image = self.explo_imgs[self.index]