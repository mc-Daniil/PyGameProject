import pygame, os, sys, random, copy
from pygame.locals import *


FPS = 60 # Частота обнвления экрана
WIDTH = 800 # Ширина окна
HEIGHT = 600 # Высота окна
H_WIDTH = int(WIDTH / 2) # Половина ширины
H_HEIGHT = int(HEIGHT / 2) # Половина высоты
TILE_W = 50 # Ширина плитки
TILE_H = 85 # Высота плитки
TILE_FH = 40
CAM_SPEED = 5 # Скорость перемещения камеры
DECOR_PER = 20 # Процент декораций

# Цвета
BLUE = (0, 170, 255)
WHITE = (255, 255, 255)
BG_COLOR = BLUE # Фон
TEXT_COLOR = WHITE # Текст


def startScreen():
    pass


def read_level(filename):
    pass


def run_level(levels, current_level):
    pass


if __name__ == '__main__':

    pygame.init() # Инициализация pygame
    FPS_CLOCK = pygame.time.Clock() # Часы FPS

    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT)) # Разрешение экрана

    pygame.display.set_caption("Star") # Название экрана
    FONT = pygame.font.Font(None, 18) # Шрифт

    # Картинки
    IMAGES = {'uncovered goal': pygame.image.load('data/Images/RedSelector.png'),
                  'covered goal': pygame.image.load('data/Images/Selector.png'),
                  'star': pygame.image.load('data/Images/Star.png'),
                  'corner': pygame.image.load('data/Images/Wall_Block_Tall.png'),
                  'wall': pygame.image.load('data/Images/Wood_Block_Tall.png'),
                  'inside floor': pygame.image.load('data/Images/Plain_Block.png'),
                  'outside floor': pygame.image.load('data/Images/Grass_Block.png'),
                  'title': pygame.image.load('data/Images/star_title.png'),
                  'solved': pygame.image.load('data/Images/star_solved.png'),
                  'princess': pygame.image.load('data/Images/princess.png'),
                  'boy': pygame.image.load('data/Images/boy.png'),
                  'catgirl': pygame.image.load('data/Images/catgirl.png'),
                  'horngirl': pygame.image.load('data/Images/horngirl.png'),
                  'pinkgirl': pygame.image.load('data/Images/pinkgirl.png'),
                  'rock': pygame.image.load('data/Images/Rock.png'),
                  'short tree': pygame.image.load('data/Images/Tree_Short.png'),
                  'tall tree': pygame.image.load('data/Images/Tree_Tall.png'),
                  'ugly tree': pygame.image.load('data/Images/Tree_Ugly.png')}

    # Объекты в зависимости от символа в файле с уровнем
    OBJECTS = {'x': IMAGES['corner'],
                   '#': IMAGES['wall'],
                   'o': IMAGES['inside floor'],
                   ' ': IMAGES['outside floor']}

    # Объекты для декора
    DECOR = {'1': IMAGES['rock'],
                          '2': IMAGES['short tree'],
                          '3': IMAGES['tall tree'],
                          '4': IMAGES['ugly tree']}

    # Изображения возможных персонажей
    current_player = 0
    PLAYERS = [IMAGES['princess'],
                    IMAGES['boy'],
                    IMAGES['catgirl'],
                    IMAGES['horngirl'],
                    IMAGES['pinkgirl']]

    startScreen() # Показать начальный экран

    # Считывание уровней из файлов и создание массива с уровнями
    level1 = read_level("data/Levels/level_1.txt")
    level2 = read_level("data/Levels/level_2.txt")
    level3 = read_level("data/Levels/level_3.txt")
    level4 = read_level("data/Levels/level_4.txt")
    level5 = read_level("data/Levels/level_5.txt")
    levels = [level1, level2, level3, level4, level5]
    current_level = 0 # Текущий уровень

    # Основной игровой цикл
    while True:
        res = run_level(levels, current_level)

        if res in ("solved", "next"):
            current_level += 1
            if current_level >= len(levels):
                current_level = 0
        elif res == "back":
            current_level -= 1
            if current_level < 0:
                current_level = len(levels) - 1












