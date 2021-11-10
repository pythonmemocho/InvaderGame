import pygame as pg
from pygame.locals import *
from setting import *
import random


class Enemy(pg.sprite.Sprite):
    def __init__(self,x,y,color) -> None:
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.width = self.image.get_width()
        #色は引数で設定しておきインスタンス化の時に選ぶ
        self.image.fill(color)
        self.speed = 5
        #動きのタイミング用タイマー、カウント
        self.timing_counter = 30
        self.timing_count = 0
        self.move_count = 0

    #横移動用のメソッド
    def Xmove(self,speed):
        self.rect.x += speed
        self.timing_counter = 30
        self.timing_count += 1
        return self.rect.x,self.timing_counter,self.timing_count

    #縦移動用のメソッド
    def Ymove(self):
        self.rect.y += 20
        self.timing_counter = 30
        self.timing_count += 1
        return self.rect.y,self.timing_counter,self.timing_count

    #弾丸発射用のメソッド（クラスのインスタンス化を返す）
    def shot(self,pos):
        return Bullet(pos)

    #毎フレームのupdate
    def update(self):
        #タイミングをカウントダウンし、0になればmove_countをアップする
        #1~5までx,6でy,7~11でx,12でy移動
        self.timing_counter -= 1
        if self.timing_counter < 0:
            self.move_count += 1
            if self.move_count <= 5:
                self.Xmove(5)
            elif self.move_count == 6:
                self.Ymove()
            elif self.move_count >= 7 and self.move_count <= 11:
                self.Xmove(-5)
            elif self.move_count == 12:
                self.Ymove()
                self.move_count = 0
        

class Bullet(pg.sprite.Sprite):
    def __init__(self,pos) -> None:
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((5,15))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (pos)
    
    def update(self):
        self.rect.y += 10
        #弾丸が画面から消えたらスプライトグループから削除
        if self.rect.top > HEIGHT:
            self.kill()