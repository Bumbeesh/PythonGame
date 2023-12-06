import pygame
from pygame.math import Vector2
import math
from enemyStats import enemy_data
import settings

class Enemy(pygame.sprite.Sprite):
    def __init__(self,enemy_type,waypounts, images):
        pygame.sprite.Sprite.__init__(self)
        self.waypoints = waypounts
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = enemy_data.get(enemy_type)["health"]
        self.speed = enemy_data.get(enemy_type)["speed"]
        self.angle = 0
        self.original_image = images.get(enemy_type)
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self,world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self,world):
        #Определение таргета
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            #Враг достиг конца
            self.kill()
            world.health -= 5
            world.missed_enemy += 1

        #Вычисление дистанции до таргета
        distance = self.movement.length()
        #Проверка - оставшаяся длина больше скорости
        if distance >= self.speed:
            self.pos += (self.movement.normalize()) * self.speed
        else:
            if distance != 0:
                self.pos += (self.movement.normalize()) * distance
            self.target_waypoint += 1


    def rotate(self):
        #Дистанция до следующего поинта
        distance = self.target - self.pos
        self.angle = math.degrees(math.atan2(-distance[1],distance[0]))

        #Поворот картинки и обновление границы
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            world.money += settings.KILL_GAIN_MONEY
            self.kill()
            world.killed_enemy += 1
