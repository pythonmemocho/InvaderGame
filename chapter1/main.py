import pygame as pg
from pygame.locals import *
from enemy import Enemy
from setting import *
from player import *
from enemy import *
from title_screen import Title
import random

class Main:
    def __init__(self) -> None:
        pg.init()
        
        #プレイヤーのインスタンス化
        self.player = Player(WIDTH // 2,HEIGHT - 50)
        #各スプライトグループを設定
        self.playerSprite = pg.sprite.GroupSingle(self.player)
        self.enemySprite = pg.sprite.Group()
        #敵の配置（ループで４列作成）
        for i in range(4):
            for j in range(10):
                self.enemy = Enemy(30 + 42*j, 80 + 36*i,COLORS[i])
                self.enemySprite.add(self.enemy)
        #敵の弾丸のグループも作成しておく（グループの中身はまだ空）
        self.enemybulletSprite = pg.sprite.Group()

        #現在の状態、0=タイトル画面, 1=ゲーム実行中,3=ゲームオーバー,4=ゲームクリア
        self.game_condition = 0
        #画面切り替え用のタイマー
        self.timer = 50
        #得点
        self.score = 0
        #敵の弾丸発射間隔
        self.enemy_bullet_timer = 50

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
                self.enemy = Enemy(30 + 42*j, 80 + 36*i,COLORS[i])
                self.enemySprite.add(self.enemy)

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

                #スコア表示の描画
                draw_text(f'SCORE: {self.score}', 30, WIDTH // 6, 8, WHITE) 

                #弾丸と敵キャラの衝突判定
                #groupcollideは衝突判定があった場合リストを返してくるので、リストに何か入った時点で衝突判定があったと判断できる
                if len(pg.sprite.groupcollide(self.enemySprite,self.player.bulletSprite,True,True)) > 0:
                    self.score += 100

                #敵の弾丸とプレイヤーの衝突判定(判定条件は上と同じ)
                if len(pg.sprite.groupcollide(self.playerSprite,self.enemybulletSprite,False,False)) > 0:
                    self.game_condition = 3

                #自機と敵キャラの衝突判定
                for enemy in self.enemySprite:
                    if pg.sprite.collide_rect(enemy,self.player):
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

            #3：ゲームオーバーの時の処理
            elif self.game_condition == 3:
                #画面切り替えのタイマーを作業し、タイマーが切れたらゲーム状態を変更
                self.timer -= 1
                if self.timer < 0:
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