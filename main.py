import random, sys, copy, pygame
from pygame.locals import *

FPS = 60
WIDTH = 800 # Ширина окна игры
HEIGHT = 600 # Высота окна игры
HALF_WIDTH = int(WIDTH / 2)
HALF_HEIGHT = int(HEIGHT / 2)

# Параметры плиток
TILE_WIDTH = 50
TILE_HEIGHT = 85
TILE_FLOOR_HEIGHT = 40

CAM_SPEED = 5 # скорость камеры

# Процент декораций
DECOR_PER = 20

BLUE = (0, 170, 255)
WHITE = (255, 255, 255)
BG_COLOR = BLUE
TEXT_COLOR = WHITE

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"


def run_level(levels, levelNum):
    """
    Запуск уровня
    :param levels:
    :param levelNum:
    :return:
    """
    global currentImage

    level_o = levels[levelNum]
    mapObj = decorateMap(level_o["mapObj"], level_o["startState"]["player"])
    gameStateObj = copy.deepcopy(level_o["startState"])
    mapNeedsRedraw = True # Чтобы сработала drawMap()
    levelSurf = BASICFONT.render(f"Level {levelNum + 1} of {len(levels)}", 1, TEXT_COLOR)
    levelRect = levelSurf.get_rect()
    levelRect.bottomleft = (20, HEIGHT - 35)
    mapWidth = len(mapObj) * TILE_WIDTH
    mapHeight = (len(mapObj[0]) - 1) * TILE_FLOOR_HEIGHT + TILE_HEIGHT
    MAX_CAM_X_PAN = abs(HALF_HEIGHT - int(mapHeight / 2)) + TILE_WIDTH
    MAX_CAM_Y_PAN = abs(HALF_WIDTH - int(mapWidth / 2)) + TILE_HEIGHT

    levelIsComplete = False
    # Сколько двигалась камера
    cameraOffsetX = 0
    cameraOffsetY = 0
    # Нажаты ли клавишы для перемещения
    cameraUp = False
    cameraDown = False
    cameraLeft = False
    cameraRight = False

    while True: # основной цикл игры
        playerMoveTo = None
        keyPressed = False

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                keyPressed = True
                if event.key == K_LEFT:
                    playerMoveTo = LEFT
                elif event.key == K_RIGHT:
                    playerMoveTo = RIGHT
                elif event.key == K_UP:
                    playerMoveTo = UP
                elif event.key == K_DOWN:
                    playerMoveTo = DOWN
                elif event.key == K_a:
                    cameraLeft = True
                elif event.key == K_d:
                    cameraRight = True
                elif event.key == K_w:
                    cameraUp = True
                elif event.key == K_s:
                    cameraDown = True
                elif event.key == K_n:
                    return 'next'
                elif event.key == K_b:
                    return 'back'
                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_BACKSPACE:
                    return 'reset'
                elif event.key == K_p:
                    currentImage += 1
                    if currentImage >= len(PLAYERIMAGES):
                        currentImage = 0
                    mapNeedsRedraw = True
            elif event.type == KEYUP:
                if event.key == K_a:
                    cameraLeft = False
                elif event.key == K_d:
                    cameraRight = False
                elif event.key == K_w:
                    cameraUp = False
                elif event.key == K_s:
                    cameraDown = False

        if playerMoveTo != None and not levelIsComplete:
            moved = makeMove(mapObj, gameStateObj, playerMoveTo)

            if moved:
                gameStateObj['stepCounter'] += 1
                mapNeedsRedraw = True

            if isLevelFinished(level_o, gameStateObj):
                levelIsComplete = True
                keyPressed = False

        DISPLAYSURF.fill(BG_COLOR)

        if mapNeedsRedraw:
            mapSurf = drawMap(mapObj, gameStateObj, level_o['goals'])
            mapNeedsRedraw = False

        if cameraUp and cameraOffsetY < MAX_CAM_X_PAN:
            cameraOffsetY += CAM_SPEED
        elif cameraDown and cameraOffsetY > -MAX_CAM_X_PAN:
            cameraOffsetY -= CAM_SPEED
        if cameraLeft and cameraOffsetX < MAX_CAM_Y_PAN:
            cameraOffsetX += CAM_SPEED
        elif cameraRight and cameraOffsetX > -MAX_CAM_Y_PAN:
            cameraOffsetX -= CAM_SPEED

        mapSurfRect = mapSurf.get_rect()
        mapSurfRect.center = (HALF_WIDTH + cameraOffsetX, HALF_HEIGHT + cameraOffsetY)

        DISPLAYSURF.blit(mapSurf, mapSurfRect)

        DISPLAYSURF.blit(levelSurf, levelRect)
        stepSurf = BASICFONT.render(f"Steps: {gameStateObj['stepCounter']}", 1, TEXT_COLOR)
        stepRect = stepSurf.get_rect()
        stepRect.bottomleft = (20, HEIGHT - 10)
        DISPLAYSURF.blit(stepSurf, stepRect)

        if levelIsComplete:
            solvedRect = IMAGESDICT['solved'].get_rect()
            solvedRect.center = (HALF_WIDTH, HALF_HEIGHT)
            DISPLAYSURF.blit(IMAGESDICT['solved'], solvedRect)

            if keyPressed:
                return 'solved'

        pygame.display.update()
        FPSCLOCK.tick()


def isWall(mapObj, x, y):
    """
    Смотрит, на стенке игрок или нет
    :param mapObj:
    :param x:
    :param y:
    :return:
    """
    if x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return False
    elif mapObj[x][y] in ('#', 'x'):
        return True
    return False


def decorateMap(mapObj, startxy):
    """
    Копирует карту, полностью рисует с игроком и возвращает
    :param mapObj:
    :param startxy:
    :return:
    """

    startx, starty = startxy

    mapObjCopy = copy.deepcopy(mapObj)

    for x in range(len(mapObjCopy)):
        for y in range(len(mapObjCopy[0])):
            if mapObjCopy[x][y] in ('$', '.', '@', '+', '*'):
                mapObjCopy[x][y] = ' '

    floodFill(mapObjCopy, startx, starty, ' ', 'o')

    for x in range(len(mapObjCopy)):
        for y in range(len(mapObjCopy[0])):

            if mapObjCopy[x][y] == '#':
                if (isWall(mapObjCopy, x, y-1) and isWall(mapObjCopy, x+1, y)) or \
                   (isWall(mapObjCopy, x+1, y) and isWall(mapObjCopy, x, y+1)) or \
                   (isWall(mapObjCopy, x, y+1) and isWall(mapObjCopy, x-1, y)) or \
                   (isWall(mapObjCopy, x-1, y) and isWall(mapObjCopy, x, y-1)):
                    mapObjCopy[x][y] = 'x'

            elif mapObjCopy[x][y] == ' ' and random.randint(0, 99) < DECOR_PER:
                mapObjCopy[x][y] = random.choice(list(OUTSIDEDECOMAPPING.keys()))

    return mapObjCopy


def isBlocked(mapObj, gameStateObj, x, y):
    """
    Можно ли идти дальше или нет
    :param mapObj:
    :param gameStateObj:
    :param x:
    :param y:
    :return:
    """

    if isWall(mapObj, x, y):
        return True

    elif x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return True

    elif (x, y) in gameStateObj['stars']:
        return True

    return False


def makeMove(mapObj, gameStateObj, playerMoveTo):
    """
    Сделать ход, если это можно
    :param mapObj:
    :param gameStateObj:
    :param playerMoveTo:
    :return:
    """

    playerx, playery = gameStateObj['player']

    stars = gameStateObj['stars']

    if playerMoveTo == UP:
        xOffset = 0
        yOffset = -1
    elif playerMoveTo == RIGHT:
        xOffset = 1
        yOffset = 0
    elif playerMoveTo == DOWN:
        xOffset = 0
        yOffset = 1
    elif playerMoveTo == LEFT:
        xOffset = -1
        yOffset = 0

    if isWall(mapObj, playerx + xOffset, playery + yOffset):
        return False
    else:
        if (playerx + xOffset, playery + yOffset) in stars:
            if not isBlocked(mapObj, gameStateObj, playerx + (xOffset*2), playery + (yOffset*2)):
                ind = stars.index((playerx + xOffset, playery + yOffset))
                stars[ind] = (stars[ind][0] + xOffset, stars[ind][1] + yOffset)
            else:
                return False
        gameStateObj['player'] = (playerx + xOffset, playery + yOffset)
        return True


def startScreen():
    """
    Нарисовать начальный экран
    :return:
    """

    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 50
    titleRect.top = topCoord
    titleRect.centerx = HALF_WIDTH
    topCoord += titleRect.height

    instructionText = ['Притащи звёзды на их места',
                       'Стрелочки для перемещения, WASD для движения камеры, P для смены скина.',
                       'Backspace чтобы начать уровень сначала, Esc чтобы выйти.',
                       'N для перехода на следующий уровень, B для перехода на предыдущий уровень.']

    DISPLAYSURF.fill(BG_COLOR)

    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXT_COLOR)
        instRect = instSurf.get_rect()
        topCoord += 10
        instRect.top = topCoord
        instRect.centerx = HALF_WIDTH
        topCoord += instRect.height
        DISPLAYSURF.blit(instSurf, instRect)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

        pygame.display.update()
        FPSCLOCK.tick()


def readLevelsFile(filename):
    """
    Прочитать уровень из файла
    :param filename:
    :return:
    """
    mapFile = open(filename, 'r')

    content = mapFile.readlines() + ['\r\n']
    mapFile.close()

    levels = [] # Все уровни
    levelNum = 0
    mapTextLines = [] # Строки для одного уровня
    mapObj = [] # Готовая карта из символов
    for lineNum in range(len(content)):
        line = content[lineNum].rstrip('\r\n')

        if ';' in line:
            line = line[:line.find(';')]

        if line != '':
            mapTextLines.append(line)
        elif line == '' and len(mapTextLines) > 0:
            maxWidth = -1
            for i in range(len(mapTextLines)):
                if len(mapTextLines[i]) > maxWidth:
                    maxWidth = len(mapTextLines[i])
            for i in range(len(mapTextLines)):
                mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))

            for x in range(len(mapTextLines[0])):
                mapObj.append([])
            for y in range(len(mapTextLines)):
                for x in range(maxWidth):
                    mapObj[x].append(mapTextLines[y][x])

            startx = None
            starty = None
            goals = []
            stars = []
            for x in range(maxWidth):
                for y in range(len(mapObj[x])):
                    if mapObj[x][y] in ('@', '+'):
                        startx = x
                        starty = y
                    if mapObj[x][y] in ('.', '+', '*'):
                        goals.append((x, y))
                    if mapObj[x][y] in ('$', '*'):
                        stars.append((x, y))

            gameStateObj = {'player': (startx, starty),
                            'stepCounter': 0,
                            'stars': stars}
            levelObj = {'width': maxWidth,
                        'height': len(mapObj),
                        'mapObj': mapObj,
                        'goals': goals,
                        'startState': gameStateObj}

            levels.append(levelObj)

            mapTextLines = []
            mapObj = []
            gameStateObj = {}
            levelNum += 1
    return levels


def floodFill(mapObj, x, y, oldCharacter, newCharacter):
    """
    Меняет значения со старой позиции на новую
    :param mapObj:
    :param x:
    :param y:
    :param oldCharacter:
    :param newCharacter:
    :return:
    """

    if mapObj[x][y] == oldCharacter:
        mapObj[x][y] = newCharacter

    if x < len(mapObj) - 1 and mapObj[x+1][y] == oldCharacter:
        floodFill(mapObj, x+1, y, oldCharacter, newCharacter) # Право
    if x > 0 and mapObj[x-1][y] == oldCharacter:
        floodFill(mapObj, x-1, y, oldCharacter, newCharacter) # Лево
    if y < len(mapObj[x]) - 1 and mapObj[x][y+1] == oldCharacter:
        floodFill(mapObj, x, y+1, oldCharacter, newCharacter) # Низ
    if y > 0 and mapObj[x][y-1] == oldCharacter:
        floodFill(mapObj, x, y-1, oldCharacter, newCharacter) # Верх


def drawMap(mapObj, gameStateObj, goals):
    """
    Только рисует и возвращает готовую карту
    :param mapObj: 
    :param gameStateObj: 
    :param goals: 
    :return: 
    """""

    # mapSurf will be the single Surface object that the tiles are drawn
    # on, so that it is easy to position the entire map on the DISPLAYSURF
    # Surface object. First, the width and height must be calculated.
    mapSurfWidth = len(mapObj) * TILE_WIDTH
    mapSurfHeight = (len(mapObj[0]) - 1) * TILE_FLOOR_HEIGHT + TILE_HEIGHT
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
    mapSurf.fill(BG_COLOR)

    for x in range(len(mapObj)):
        for y in range(len(mapObj[x])):
            spaceRect = pygame.Rect((x * TILE_WIDTH, y * TILE_FLOOR_HEIGHT, TILE_WIDTH, TILE_HEIGHT))
            if mapObj[x][y] in TILEMAPPING:
                baseTile = TILEMAPPING[mapObj[x][y]]
            elif mapObj[x][y] in OUTSIDEDECOMAPPING:
                baseTile = TILEMAPPING[' ']

            mapSurf.blit(baseTile, spaceRect)

            if mapObj[x][y] in OUTSIDEDECOMAPPING:
                mapSurf.blit(OUTSIDEDECOMAPPING[mapObj[x][y]], spaceRect)
            elif (x, y) in gameStateObj['stars']:
                if (x, y) in goals:
                    mapSurf.blit(IMAGESDICT['covered goal'], spaceRect)
                mapSurf.blit(IMAGESDICT['star'], spaceRect)
            elif (x, y) in goals:
                mapSurf.blit(IMAGESDICT['uncovered goal'], spaceRect)

            if (x, y) == gameStateObj['player']:
                mapSurf.blit(PLAYERIMAGES[currentImage], spaceRect)

    return mapSurf


def isLevelFinished(levelObj, gameStateObj):
    """
    Закончен ли уровень
    :param levelObj:
    :param gameStateObj:
    :return:
    """
    for goal in levelObj['goals']:
        if goal not in gameStateObj['stars']:
            return False
    return True


def terminate():
    """
    Закрытие окна
    :return:
    """
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption('Star Pusher')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    IMAGESDICT = {'uncovered goal': pygame.image.load('data/Images/RedSelector.png'),
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

    TILEMAPPING = {'x': IMAGESDICT['corner'],
                   '#': IMAGESDICT['wall'],
                   'o': IMAGESDICT['inside floor'],
                   ' ': IMAGESDICT['outside floor']}

    OUTSIDEDECOMAPPING = {'1': IMAGESDICT['rock'],
                          '2': IMAGESDICT['short tree'],
                          '3': IMAGESDICT['tall tree'],
                          '4': IMAGESDICT['ugly tree']}

    currentImage = 0
    PLAYERIMAGES = [IMAGESDICT['princess'],
                    IMAGESDICT['boy'],
                    IMAGESDICT['catgirl'],
                    IMAGESDICT['horngirl'],
                    IMAGESDICT['pinkgirl']]

    startScreen()

    levels = readLevelsFile('data/Levels/levels.txt')
    currentLevelIndex = 0

    while True:
        result = run_level(levels, currentLevelIndex)

        if result in ('solved', 'next'):
            currentLevelIndex += 1
            if currentLevelIndex >= len(levels):
                currentLevelIndex = 0
        elif result == 'back':
            currentLevelIndex -= 1
            if currentLevelIndex < 0:
                currentLevelIndex = len(levels) - 1
        elif result == 'reset':
            pass