import pygame

from settings import *
import math
from turret_grading import TURRET_DATA


class Turret(pygame.sprite.Sprite):
    def __init__(self,sprite_sheet,tile_x,tile_y):
        pygame.sprite.Sprite.__init__(self)

        self.upgrade_level = 1
        self.tile_x = tile_x
        self.tile_y = tile_y

        self.cd = TURRET_DATA[self.upgrade_level - 1].get('cd')
        self.range = TURRET_DATA[self.upgrade_level - 1].get('range')

        self.selected = False
        self.target = None



        self.x = (self.tile_x + 0.5) * TILE_SIZE
        self.y = (self.tile_y + 0.5) * TILE_SIZE
        self.lastshot = pygame.time.get_ticks()







        #Анимации
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

                                #Отрисовка дальности турельки
        self.range_image = pygame.Surface((self.range*2,self.range*2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pygame.draw.circle(self.range_image, 'grey100',(self.range,self.range),self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def update(self,enemy_group):
        if self.target:
            self.play_animation()
        else:
            if pygame.time.get_ticks() - self.lastshot > self.cd:
                self.pick_target(enemy_group)

    def play_animation(self):
        #Обновление картинки
        self.original_image = self.animation_list[self.frame_index]
        # Прошёл ли кд с прошлого обновления
        if pygame.time.get_ticks() - self.update_time > ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            # Возврат к началу
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                #кд может откатываться
                self.lastshot = pygame.time.get_ticks()
                self.target = None

    def pick_target(self,enemy_group):
        x_distance = 0
        y_distance = 0

        for enemy in enemy_group:
            x_distance = enemy.pos[0] - self.x
            y_distance = enemy.pos[1] - self.y
            dist = math.sqrt(x_distance**2 + y_distance**2)
            if dist < self.range:
                self.target = enemy
                self.angle = math.degrees(math.atan2(-y_distance,x_distance))

    def load_images(self):
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def upgrade(self):
        self.upgrade_level += 1
        self.cd = TURRET_DATA[self.upgrade_level - 1].get('cd')
        self.range = TURRET_DATA[self.upgrade_level - 1].get('range')

        self.range_image = pygame.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.range_image, 'grey100', (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def draw(self,surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        surface.blit(self.image,self.rect)
        if self.selected:
            surface.blit(self.range_image,self.range_rect)

