import pygame as pg
import os

class Object_base(pg.sprite.Sprite):
    def __init__(self, x, y, img_num, x_size, y_size):
        image_file_dir = os.path.join(os.path.dirname(__file__),'images')
        images_dir = [
            os.path.join(image_file_dir,"player.png"),
            os.path.join(image_file_dir,"enemy.png"),
            os.path.join(image_file_dir,"enemy_up.png"),
        ]
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(images_dir[img_num]).convert_alpha()
        self.image = pg.transform.scale(self.image,(x_size,y_size))
        self.mask = pg.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    