import pygame as pg
from pygame import transform
from pygame.locals import *
from setting import *
import random


class Enemy(pg.sprite.Sprite):
    #(削除)initの引数[color]を削除
    # def __init__(self,x,y,color) -> None:
    #(追加)画像選択用の引数indをわたす
    def __init__(self,x,y,ind) -> None:
        pg.sprite.Sprite.__init__(self)
        #(削除)画像を用意したので削除
        # self.image = pg.Surface((30,20))

        #(追加)リストに使用したい画像を入れる
        self.images = [
            pg.image.load('chapter3\images\enemy.png').convert_alpha(),
            pg.image.load('chapter3\images\enemy_up.png').convert_alpha()
        ]
        #(追加)画像選択用のindexを用意。値はインスタンス化の時の引数で指定
        self.index = ind
        self.image = self.images[self.index]
        #(追加)画像のサイズを設定
        self.image = pg.transform.scale(self.image,(40,32))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.width = self.image.get_width()

        #(削除)カラーの設定も不要なので削除
        # self.image.fill(color)
        
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