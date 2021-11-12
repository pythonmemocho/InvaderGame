import pygame as pg
from pygame.locals import *
from enemy import Enemy
from setting import *
from player import *
from enemy import *
from title_screen import Title
import random
from barrier import *
from explo import *


class Main:
    def __init__(self) -> None:
        pg.init()

        #プレイヤーのインスタンス化
        self.player = Player(WIDTH // 2,HEIGHT - 50)
        #各スプライトグループを設定
        self.playerSprite = pg.sprite.GroupSingle(self.player)
        self.enemySprite = pg.sprite.Group()

        #バリアと爆発演出用のグループを設定
        self.barrierSprite = pg.sprite.Group()
        self.exploSprite = pg.sprite.Group()

        #敵の配置（ループで４列作成）
        for i in range(4):
            for j in range(10):
                #(削除)色の引数設定は不要なので削除。画像に合わせて少し描画位置を調整
                # self.enemy = Enemy(30 + 42*j, 80 + 36*i,COLORS[i])
                #(追加)3番目の引数にindexを指定して画像を選択
                self.enemy = Enemy(28 + 44*j, 80 + 36*i,0)
                self.enemySprite.add(self.enemy)
        #敵の弾丸のグループも作成しておく（グループの中身はまだ空）
        self.enemybulletSprite = pg.sprite.Group()

        #バリアの生成
        self.create_barrier()

        #現在の状態、0=タイトル画面, 1=ゲーム実行中,3=ゲームオーバー,4=ゲームクリア
        self.game_condition = 0
        #画面切り替え用のタイマー
        self.timer = 50
        #得点
        self.score = 0
        #敵の弾丸発射間隔
        self.enemy_bullet_timer = 50

        #自機が敵の弾丸に当たった時のフラグ
        self.hit = False
        
    #バリア生成用のメソッドを作成
    def create_barrier(self):
        #4つ配置するので、range(4)
        for ind in range(4):
            #barrier.pyのshapeリストに沿って、[ 1 ]の場合にクラスをインスタンス化する
            for i, row in enumerate(shape):
                for j, col in enumerate(row):
                    if col == 1:
                        barrier = Barrier(j*5+32+(ind*(WIDTH // 4)),i*10+(HEIGHT-120))
                        self.barrierSprite.add(barrier)
        return barrier,self.barrierSprite

    #リスタート処理時実行するメソッド
    def restart(self):
        self.game_condition = 1
        self.timer = 50
        self.score = 0
        self.enemy_bullet_timer = 50
        #プレイヤーを再インスタンス化
        self.player = Player(WIDTH // 2,HEIGHT - 50)
        self.playerSprite = pg.sprite.GroupSingle(self.player)
        self.enemybulletSprite = pg.sprite.Group()
        #敵のスプライトグループを空にして、再度入れる
        self.enemySprite.empty()
        for i in range(4):
            for j in range(10):
                #(削除)色の引数設定は不要なので削除。画像に合わせて少し描画位置を調整
                # self.enemy = Enemy(30 + 42*j, 80 + 36*i,COLORS[i])
                #(追加)3番目の引数にindexを指定して画像を選択
                self.enemy = Enemy(28 + 44*j, 80 + 36*i,0)
                self.enemySprite.add(self.enemy)

        #バリアのスプライトグループを空にして、再度メソッドを実行
        self.barrierSprite.empty()
        self.create_barrier()

    #メインループ処理
    def main(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if  event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            #0：タイトル画面表示
            if self.game_condition == 0:
                #タイトル画面の呼び出し
                title = Title()
                #任意のキーでゲームスタート
                if pg.key.get_pressed()[K_s]:
                    self.game_condition = 1

            #1：ゲーム実行
            elif self.game_condition == 1: 
                #マウスカーソルの削除
                pg.mouse.set_visible(False)
                #画面を黒に塗る
                SCREEN.fill(BLACK)

                #敵の弾丸生成
                self.enemy_bullet_timer -= 1
                #敵の弾丸の発射間隔が0になったら実行
                if self.enemy_bullet_timer < 0:
                    #現在の敵の位置をリストに格納
                    li = [x for x in self.enemySprite]
                    #敵の数が1以上なら
                    if len(li) > 0:
                        #上のリストからランダムに選び、rectを取得
                        enemy_random = random.choice(li)
                        pos = enemy_random.rect.center
                        #取得したrectの位置にメソッドを実行し、タイマーをもどす
                        self.enemybulletSprite.add(self.enemy.shot(pos))
                        self.enemy_bullet_timer = 50
                
                #スプライトの描画
                self.enemybulletSprite.draw(SCREEN)
                self.enemySprite.draw(SCREEN)
                self.playerSprite.draw(SCREEN)
                
                #(追加)バリアと爆発の描画
                self.barrierSprite.draw(SCREEN)
                self.exploSprite.draw(SCREEN)

                #スコア表示の描画
                draw_text(f'SCORE: {self.score}', 30, WIDTH // 6, 8, WHITE) 

                #弾丸と敵キャラの衝突判定＋爆発演出
                for collide in pg.sprite.groupcollide(self.enemySprite,self.player.bulletSprite,True,True):
                    explosion = Explosion(collide.rect.center)
                    self.exploSprite.add(explosion)
                    self.score += 100

                #敵の弾丸とプレイヤーの衝突判定＋爆発演出
                #(追加)groupcollideの引数にcollide_maskを追記する
                for collide in pg.sprite.groupcollide(self.playerSprite,self.enemybulletSprite,True,True,pg.sprite.collide_mask):
                    explosion = Explosion(collide.rect.center)
                    self.exploSprite.add(explosion)
                    #フラグを起こす
                    self.hit = True
                if self.hit:
                    #こちらでカウントダウンして少し間を持たせないと、自機の爆発演出が表示されない
                    self.timer -= 1
                    if self.timer < 0:
                        self.game_condition = 3


                #弾丸・敵とバリアの衝突判定
                pg.sprite.groupcollide(self.player.bulletSprite,self.barrierSprite,True,True)
                pg.sprite.groupcollide(self.enemybulletSprite,self.barrierSprite,True,True)
                pg.sprite.groupcollide(self.enemySprite,self.barrierSprite,False,True)

                #自機と敵キャラの衝突判定
                for enemy in self.enemySprite:
                    #(削除)maskに当たり判定を変更したいので、collide_rectを削除
                    # if pg.sprite.collide_rect(enemy,self.player):

                    #(追加)collide_rectからcollide_maskに変更
                    if pg.sprite.collide_mask(enemy,self.player):
                        #プレイヤースプライトを削除し、ゲーム状態を変更
                        self.player.kill()
                        self.game_condition = 3

                #敵を全て殲滅した時の処理
                if len(self.enemySprite) <= 0:
                    #画面切り替えのタイマーを作業し、タイマーが切れたらゲーム状態を変更
                    self.timer -= 1
                    if self.timer < 0:
                        self.game_condition = 4

                #スプライトのupdate処理
                self.enemybulletSprite.update()
                self.enemySprite.update()
                self.playerSprite.update()

                self.exploSprite.update()

            #3：ゲームオーバーの時の処理
            elif self.game_condition == 3:
                self.hit = False
                SCREEN.fill(BLACK)
                draw_text(f'Game Over', 60, WIDTH / 2, int(HEIGHT * 0.45), RED)
                draw_text(f'[ R ]key Restart', 30, WIDTH / 2, int(HEIGHT * 0.60), RED)
                #任意のキーでリスタート
                if pg.key.get_pressed()[K_r]:
                    self.restart()

            #ゲームクリアの時の処理
            elif self.game_condition == 4:
                #画面切り替えのタイマーを作業し、タイマーが切れたらゲーム状態を変更
                self.timer -= 1
                if self.timer < 0:
                    SCREEN.fill(BLACK)
                    draw_text(f'GAME CLEAR!', 60, WIDTH / 2, int(HEIGHT * 0.45), YELLOW)
                    draw_text(f'[ R ]key Restart', 30, WIDTH / 2, int(HEIGHT * 0.60), YELLOW)
                #任意のキーでリスタート
                if pg.key.get_pressed()[K_r]:
                    self.restart()

            pg.display.update()
            CLOCK.tick(FPS)
        pg.quit()

main = Main()


if __name__ == "__main__":
    main.main()