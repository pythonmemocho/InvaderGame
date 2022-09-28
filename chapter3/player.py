import pygame as pg
from pygame.locals import *
from setting import *

class Object_base(pg.sprite.Sprite):
    def __init__(self, x, y, img_num):
        pg.sprite.Sprite.__init__(self)
        images_dir = [
            "chapter3\images\player.png",
            "chapter3\images\enemy.png",
            "chapter3\images\enemy_up.png",
            "chapter3\images\explosion.png"
        ]
        self.image = pg.image.load(images_dir[img_num]).convert_alpha()
        self.image = pg.transform.scale(self.image,(40,32))
        self.mask = pg.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()


class Player(Object_base):
    def __init__(self,x,y,img_num) -> None:
        super().__init__(x, y, img_num)

        self.speed = 5
        #弾丸の発射用の変数
        self.bullet_ready = True
        self.bullet_cooldown = 10
        #弾丸のスプライトグループを作成しておく（中身は空）
        self.bulletSprite = pg.sprite.Group()
    
    #shotメソッドを実行したら、弾丸クラスをインスタンス化し、返す
    def shot(self):
        return Bullet(self.rect.x + self.width // 2, self.rect.y)

    def update(self):
        #キー操作処理
        key = pg.key.get_pressed()
        if key[K_d]:
            if self.rect.right < WIDTH:
                self.rect.x += self.speed
        if key[K_a]:
            if self.rect.left > 0:
                self.rect.x -= self.speed

        #スペースキーが押されたらbulletクラスをインスタンス化する
        if key[K_UP]:
            #弾丸が発射できる間隔を限定しておく
            if self.bullet_ready and len(self.bulletSprite) == 0:
                self.bulletSprite.add(self.shot())
                self.bullet_ready = False
                
        #弾丸スプライトグループの描画
        self.bulletSprite.draw(SCREEN)
        
        #弾丸発射可能の間隔
        if not self.bullet_ready:
            self.bullet_cooldown -= 1
        if self.bullet_cooldown < 0:
            self.bullet_ready = True
            self.bullet_cooldown = 10
        
        #弾丸のスプライトグループupdate
        self.bulletSprite.update()

class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y) -> None:
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((5,15))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def update(self):
        self.rect.y -= 15
        #弾丸が画面から消えたらスプライトグループから削除
        if self.rect.y < 0:
            self.kill()

    