import pygame
from enemyStats import enemy_spawn_data
import random
import settings
class World():
    def __init__(self,data, map_image):
        self.level = 1
        self.health = settings.HEALTH
        self.money = settings.MONEY
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.image = map_image
        self.enemy_list = []
        self.spawned = 0
        self.killed_enemy = 0
        self.missed_enemy = 0
#Здесь обрабатывается JSON-файл, чтобы получить x y для waypoint`a(точки, по которым ходит враг)
    def process_data(self):
        for layer in self.level_data['layers']:
            if layer['name'] == 'tilemap':
                self.tile_map = layer['data']
            if layer['name'] == 'waypoints':
                for objects in layer['objects']:
                    waypoint_data = objects['polyline']
                    self.process_waypoints(waypoint_data)

    def process_waypoints(self,data):
        for point in data:
            temporary_x = point.get('x')
            temporary_y = point.get('y')
            print((temporary_x,temporary_x))
            self.waypoints.append((temporary_x,temporary_y))

    def spawn_enemies(self):
        enemies = enemy_spawn_data[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        random.shuffle(self.enemy_list)

    def check_level_complete(self):
        if (self.killed_enemy + self.missed_enemy) == len(self.enemy_list):
            return True

    def reset_level_count(self):
        self.enemy_list = []
        self.killed_enemy = 0
        self.missed_enemy = 0
        self.spawned = 0
    def draw(self,surface):
        surface.blit(self.image,(0,0))