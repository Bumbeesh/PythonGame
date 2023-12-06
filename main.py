import pygame
import json
import time


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

game_over = False
game_pause = False
game_win_or_lost = 0 # 1 если победа, 0 - поражение
last_enemy_spawn = pygame.time.get_ticks()
start_level = False
placing_turrets = False
selected_turret = None

                                    #Картинки

#Карта
map_image = pygame.image.load('levels/level2.png').convert_alpha()

#Враги
enemy_images = {
    'weak':pygame.image.load('assets/enemies/enemy_1.png').convert_alpha(),
'medium':pygame.image.load('assets/enemies/enemy_2.png').convert_alpha(),
'strong':pygame.image.load('assets/enemies/enemy_3.png').convert_alpha(),
'elite':pygame.image.load('assets/enemies/enemy_4.png').convert_alpha()
}

#Турелька
cursor_turret = pygame.image.load('assets/images/turrets/cursor_turret.png')

#Кнопки
buy_turrets_image = pygame.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pygame.image.load('assets/images/buttons/cancel.png').convert_alpha()
grade_turrets_image = pygame.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
begin_game_image = pygame.image.load('assets/images/buttons/begin.png')
restart_game_image = pygame.image.load('assets/images/buttons/restart.png')
fast_game_image = pygame.image.load('assets/images/buttons/fast_forward.png')
heart_image = pygame.image.load('assets/images/gui/heart.png')
money_image = pygame.image.load('assets/images/gui/coin.png')
pause_image = pygame.image.load('assets/images/buttons/pause.png')
resume_image = pygame.image.load('assets/images/gui/coin.png')

#Звук
shot_sound = pygame.mixer.Sound('assets/audio/shot.wav')
shot_sound.set_volume(0.5)

#Анимация
turret_sheet = pygame.image.load('assets/images/turrets/turret_1.png').convert_alpha()

#JSON для уровня
with open('levels/level2.tmj') as file:
    world_data = json.load(file)

#Шрифты
text_font = pygame.font.SysFont("Consolas",24,bold = True)
large_font = pygame.font.SysFont("Consolas",36)

#Отрисовка текста
def draw_text(text,font,text_col,x,y):
    image = font.render(text, True, text_col)
    screen.blit(image,(x,y))

#Интерфейс(хп,деньги,уровень)
def GUI():
    pygame.draw.rect(screen,'maroon',(screen_w,0,settings.SIDE_PANEL,screen_h))
    pygame.draw.rect(screen,'grey0',(screen_w,0,settings.SIDE_PANEL,400),2)
    draw_text("LEVEL: " + str(world.level), text_font, "grey100", screen_w + 10, 10)
    screen.blit(heart_image, (screen_w + 10, 35))
    draw_text(str(world.health), text_font, "grey100", screen_w + 50, 40)
    screen.blit(money_image, (screen_w + 10, 65))
    draw_text(str(world.money), text_font, "grey100", screen_w + 50, 70)

#Создание турели
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
            new_turret = Turret(turret_sheet, mouse_tile_x, mouse_tile_y,shot_sound)
            turret_group.add(new_turret)
            world.money -= settings.BUY_TURRET_COST

#Выбор турели
def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // TILE_SIZE
    mouse_tile_y = mouse_pos[1] // TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

#Очистка выбора(исчезновение белой зоны)
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

#Кнопки
turret_button = Button(screen_w + 30, 120, buy_turrets_image,True)
cancel_turret_button = Button(screen_w + 50, 180, cancel_image,True)
grade_button = Button(screen_w + 5, 180, grade_turrets_image,True)
begin_button = Button(screen_w + 60, 300, begin_game_image,True)
restart_button = Button(310, 300, restart_game_image,True)
fast_game_button = Button(screen_w+50, 300, fast_game_image,False)
pause_game_button = Button(0,0,pause_image,True)
resume_game_button = Button(70,0,resume_image,True)

# Игровой цикл
run = True
while run:



    clock.tick(FPS)

    #ОБНОВЛЕНИЕ#

    if not(game_over):
        if world.health <= 0:
            game_over = True
            game_win_or_lost = -1
        if world.level > settings.LEVEL_COUNT:
            game_over = True
            game_win_or_lost = 1



#Отрисовка турели и врагов
        enemy_group.update(world)
        turret_group.update(enemy_group,world)

        if selected_turret:
            selected_turret.selected = True


    #ОТРИСОВКА#

    #Отрисовка уровня
    world.draw(screen)

    #Отрисовка пути врагов
    enemy_group.draw(screen)

    for turret in turret_group:
        turret.draw(screen)
    turret_group.draw(screen)

    GUI()

    if not(game_over):

        #Проверка на старт уровня
        if not(start_level):
            if begin_button.draw(screen):
                start_level = True
        else:
            #Ускорение игры
            world.game_speed = 1
            if fast_game_button.draw(screen):
                world.game_speed = 2
            if pygame.time.get_ticks() - last_enemy_spawn > settings.SPAWN_RATE:
                if world.spawned < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned]
                    enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                    enemy_group.add(enemy)
                    world.spawned += 1
                    last_enemy_spawn = pygame.time.get_ticks()

        #Проверка завершения волны
        if world.check_level_complete():
            world.level += 1
            start_level = False
            last_enemy_spawn = pygame.time.get_ticks()
            world.reset_level_count()
            world.spawn_enemies()
            world.money += settings.LEVEL_COMPLETE_GAIN


        #Отрисовка кнопок
        draw_text(str(settings.BUY_TURRET_COST),text_font,"grey100",screen_w+215,135)
        screen.blit(money_image,(screen_w+260,130))



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
                draw_text(str(settings.UPGRADE_TURRET_COST), text_font, "grey100", screen_w + 215, 195)
                screen.blit(money_image, (screen_w + 260, 190))
                if grade_button.draw(screen):
                    if world.money >= settings.UPGRADE_TURRET_COST:
                        selected_turret.upgrade()
                        world.money -= settings.UPGRADE_TURRET_COST
    else:
        pygame.draw.rect(screen,"dodgerblue",(200,200,400,200),border_radius=30)
        if game_win_or_lost == -1:
            draw_text("GAME OVER", large_font,"grey0",310,230)
        elif game_win_or_lost == 1:
            draw_text("WIN!", large_font,"grey0",370,230)

#Рестарт(обнуление всего)
        if restart_button.draw(screen):
            game_over = False
            start_level = False
            placing_turrets = False
            selected_turret = None
            last_enemy_spawn = pygame.time.get_ticks()
            world = World(world_data,map_image)
            world.process_data()
            world.spawn_enemies()

            enemy_group.empty()
            turret_group.empty()





    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_pause = True
            print('123')
        if keys[pygame.K_SPACE]:
            game_pause = False
            print('321')
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            #Проверка - мышь в зоне приложения
            if mouse_pos[0] < screen_w and mouse_pos[1] < screen_h:
                selected_turret = None
                clear_select()
                if placing_turrets:
                    if world.money >= settings.BUY_TURRET_COST:
                        create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)



    pygame.display.flip()


pygame.quit()
