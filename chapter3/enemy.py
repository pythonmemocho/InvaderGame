import random
import os

import pygame as pg

from _object import *
from setting import *


class Enemy(Object_base):
    def __init__(self,x,y,img_num,x_size,y_size,ind) -> None:
        super().__init__(x,y,img_num,x_size,y_size)
        _file_dir = os.path.dirname(__file__)

# class Enemy(pg.sprite.Sprite):
#     def __init__(self,x,y,ind) -> None:
#         pg.sprite.Sprite.__init__(self)


        self.images = [
            pg.image.load(os.path.join(_file_dir,'images\enemy.png')).convert_alpha(),
            pg.image.load(os.path.join(_file_dir,'images\enemy_up.png')).convert_alpha(),
        ]
        
        self.index = ind
        self.image = self.images[self.index]
        self.image = pg.transform.scale(self.image,(x_size,y_size))

        # self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        # self.width = self.image.get_width()

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
        #(追加)indexをプラスしてimageに返す。indexがリストの要素数を超えるようなら0に戻す
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        #(追加)self.imageをreturnに追加する
        return self.rect.x,self.timing_counter,self.timing_count,self.image

    #縦移動用のメソッド
    def Ymove(self):
        self.rect.y += 20
        self.timing_counter = 30
        self.timing_count += 1
        #(追加)indexをプラスしてimageに返す。indexがリストの要素数を超えるようなら0に戻す
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        #(追加)self.imageをreturnに追加する
        return self.rect.y,self.timing_counter,self.timing_count,self.image

    #弾丸発射用のメソッド（クラスのインスタンス化を返す）
    def shot(self,pos):
        return Bullet(pos)
    
    def assign(self):
        pass

    #毎フレームのupdate
    def update(self):
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
            
# def enemy_set_position(a,b,g):
#     for i in range(4):
#             for j in range(10):
#                 #(追加)3番目の引数にindexを指定して画像を選択
#                 b = a(28 + 44*j, 80 + 36*i,0)
#                 g.add(b)
