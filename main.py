import pygame
import json

import settings
from settings import *
from Enemy import Enemy
from world import World
from Turret import Turret
from button import Button

pygame.init()

#Создание часов
clock = pygame.time.Clock()

# Создание экрана
screen = pygame.display.set_mode((screen_w+SIDE_PANEL,screen_h))
pygame.display.set_caption("Game")


last_enemy_spawn = pygame.time.get_ticks()
placing_turrets = False
selected_turret = None

                                    #Картинки
#Карта
map_image = pygame.image.load('levels/level.png').convert_alpha()
#Враги
enemy_images = {
    'weak':pygame.image.load('assets/enemies/enemy_1.png').convert_alpha(),
'medium':pygame.image.load('assets/enemies/enemy_2.png').convert_alpha(),
'strong':pygame.image.load('assets/enemies/enemy_3.png').convert_alpha(),
'elite':pygame.image.load('assets/enemies/enemy_4.png').convert_alpha()
}
enemy_image = pygame.image.load('assets/enemies/enemy_1.png').convert_alpha()
#Турелька
cursor_turret = pygame.image.load('assets/images/turrets/cursor_turret.png')
#Кнопки
buy_turrets_image = pygame.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pygame.image.load('assets/images/buttons/cancel.png').convert_alpha()
#Анимация
turret_sheet = pygame.image.load('assets/images/turrets/turret_1.png').convert_alpha()
grade_turrets_image = pygame.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()




#JSON для уровня
with open('levels/level.tmj') as file:
    world_data = json.load(file)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // TILE_SIZE
    mouse_tile_y = mouse_pos[1] // TILE_SIZE
    mouse_tile_num = (mouse_tile_y*COLS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == 7:
        free_space = True
        for turret in turret_group:
            if (mouse_tile_x,mouse_tile_y) == (turret.tile_x,turret.tile_y):
                free_space = False
        if free_space:
            new_turret = Turret(turret_sheet, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // TILE_SIZE
    mouse_tile_y = mouse_pos[1] // TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_select():
    for turret in turret_group:
        turret.selected = False


#Создание уровня
world = World(world_data,map_image)
world.process_data()
world.spawn_enemies( )



#Создание группы врагов
enemy_group = pygame.sprite.Group()
turret_group = pygame.sprite.Group()

turret_button = Button(screen_w + 30, 120, buy_turrets_image,True)
cancel_turret_button = Button(screen_w + 50, 180, cancel_image,True)
grade_button = Button(screen_w + 5, 180, grade_turrets_image,True)


# Игровой цикл
run = True
while run:

    clock.tick(FPS)

    #ОБНОВЛЕНИЕ#

    enemy_group.update()
    turret_group.update(enemy_group)

    if selected_turret:
        selected_turret.selected = True


    #ОТРИСОВКА#

    #Движение врага и обновление экрана(чтобы не было следа)
    screen.fill("grey100")

    #Отрисовка уровня
    world.draw(screen)

    #Отрисовка пути врагов
    enemy_group.draw(screen)

    for turret in turret_group:
        turret.draw(screen)
    turret_group.draw(screen)

    if pygame.time.get_ticks() - last_enemy_spawn > settings.SPAWN_RATE:
        enemy_type = world.enemy_list[world.spawned]
        enemy = Enemy(enemy_type, world.waypoints, enemy_images)
        enemy_group.add(enemy)
        world.spawned += 1
        last_enemy_spawn = pygame.time.get_ticks()




    #Отрисовка кнопок
    if turret_button.draw(screen):
        placing_turrets = True
    if placing_turrets:
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pygame.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= screen_w:
            screen.blit(cursor_turret,cursor_rect)
        if cancel_turret_button.draw(screen):
            placing_turrets = False
    if selected_turret:
        if selected_turret.upgrade_level < TURRET_LEVEL_MAX:
            if grade_button.draw(screen):
                selected_turret.upgrade()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            #Проверка - мышь в зоне приложения
            if mouse_pos[0] < screen_w and mouse_pos[1] < screen_h:
                selected_turret = None
                clear_select()
                if placing_turrets:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)


    pygame.display.flip()


pygame.quit()
