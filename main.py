import pygame


def draw_intro_screen(screen, i):
    """
    Экран - 0
    Рисует тексты перед запуском начального экрана
    Переход к следующему тексту по нажатию мыши
    :param screen:
    :param i:
    :return:
    """
    font = pygame.font.Font(None, 40)
    # Тексты
    texts = ["Приветствую"]
    # Отрисовка нового текста и закрашивание старого
    if i < len(texts):
        screen.fill((0, 0, 0))
        text = font.render(str(texts[i]), True, (100, 255, 100))
        x = width // 2 - text.get_width() // 2
        y = height // 2 - text.get_height() // 2
        screen.blit(text, (x, y))
    # Если нажатий больше, чем текстов, переключить на начальный экран
    else:
        global num_of_screen
        num_of_screen = 1


def draw_start_screen(screen):
    """
    Экран - 1
    Отображает кнопки начала игры и правил
    :param screen:
    :return:
    """
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)

    # Кнопка начала игры
    text1 = font.render("Начать игру", True, (100, 255, 100))
    x1 = width // 2 - text1.get_width() // 2
    y1 = height // 2 - text1.get_height()
    w1 = text1.get_width()
    h1 = text1.get_height()
    screen.blit(text1, (x1, y1))

    # Кнопка правил
    text2 = font.render("Как играть", True, (100, 255, 100))
    x2 = width // 2 - text2.get_width() // 2
    y2 = height // 2 + text2.get_height()
    w2 = text2.get_width()
    h2 = text2.get_height()
    screen.blit(text2, (x2, y2))

    # Обвести прямоугольником текст кнопок
    pygame.draw.rect(screen, (0, 255, 0), (x1 - 5, y1 - 5, w1 + 10, h1 + 10), 1)
    pygame.draw.rect(screen, (0, 255, 0), (x2 - 5, y2 - 5, w2 + 10, h2 + 10), 1)

    # Возврат координат кнопок
    return x1, y1, w1, h1, x2, y2, w2, h2


def draw_start_game(screen):
    """
    Экран - 2
    Рисует экран с набором уровней
    :param screen:
    :return:
    """
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 40)

    level1 = font.render("Уровень 1 (Кабинет физики)", True, (0, 255, 0))
    w1, h1 = level1.get_width(), level1.get_height()

    level2 = font.render("Уровень 2 (Кабинет информатики)", True, (0, 255, 0))
    w2, h2 = level2.get_width(), level2.get_height()

    level3 = font.render("Уровень 3 (Кабинет математики)", True, (0, 255, 0))
    w3, h3 = level3.get_width(), level3.get_height()

    level4 = font.render("Уровень 4 (Кабинет русского языка)", True, (0, 255, 0))
    w4, h4 = level4.get_width(), level4.get_height()

    level5 = font.render("Уровень 5 (Коридор)", True, (0, 255, 0))
    w5, h5 = level5.get_width(), level5.get_height()

    x1 = width // 2 - w1 // 2
    y1 = (height - h1 - 20 - h2 - 20 - h3 - 20 - h4 - 20 - h5) // 2

    x2 = width // 2 - w2 // 2
    y2 = y1 + h1 + 20

    x3 = width // 2 - w3 // 2
    y3 = y2 + h2 + 20

    x4 = width // 2 - w4 // 2
    y4 = y3 + h3 + 20

    x5 = width // 2 - w5 // 2
    y5 = y4 + h4 + 20

    screen.blit(level1, (x1, y1))
    screen.blit(level2, (x2, y2))
    screen.blit(level3, (x3, y3))
    screen.blit(level4, (x4, y4))
    screen.blit(level5, (x5, y5))

    pygame.draw.rect(screen, (0, 255, 0), (x1 - 5, y1 - 5, w1 + 10, h1 + 10), 1)
    pygame.draw.rect(screen, (0, 255, 0), (x2 - 5, y2 - 5, w2 + 10, h2 + 10), 1)
    pygame.draw.rect(screen, (0, 255, 0), (x3 - 5, y3 - 5, w3 + 10, h3 + 10), 1)
    pygame.draw.rect(screen, (0, 255, 0), (x4 - 5, y4 - 5, w4 + 10, h4 + 10), 1)
    pygame.draw.rect(screen, (0, 255, 0), (x5 - 5, y5 - 5, w5 + 10, h5 + 10), 1)

    return x1, y1, w1, h1, x2, y2, w2, h2, x3, y3, w3, h3, x4, y4, w4, h4, x5, y5, w5, h5



def draw_disabled_level(screen):
    """
    Показывает, что уровень недоступен, пока не пройден прошлый
    :param screen:
    :return:
    """
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 40)
    text = font.render("Чтобы попасть на этот уровень, пройдите предыдущий", True, (0, 255, 0))
    x = width // 2 - text.get_width() // 2
    y = height // 2 - text.get_height() // 2
    screen.blit(text, (x, y))


def draw_how_to_play(screen):
    """
    Экран - 3
    Показывает правила
    :param screen:
    :return:
    """
    screen.fill((255, 0, 0))
    font = pygame.font.Font(None, 30)
    text = font.render("Итак, вы оказались в школе, из которой вам нужно сбежать", True, (0, 255, 0))
    x = width // 2 - text.get_width() // 2
    y = height // 2 - text.get_height() // 2
    screen.blit(text, (x, y))


# Основа, так сказать, база, baseee
if __name__ == '__main__':
    pygame.init()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    num_of_screen = 0 # Номер экрана
    num_start_screen = 0 # Номер текста в интро

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Выход
                running = False
            if num_of_screen == 0: # Интро
                draw_intro_screen(screen, num_start_screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    num_start_screen += 1
            if num_of_screen == 1: # Стартовый экран
                x1, y1, w1, h1, x2, y2, w2, h2 = draw_start_screen(screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x in range(x1, x1 + w1) and y in range(y1, y1 + h1):
                        num_of_screen = 2
                    elif x in range(x2, x2 + w2) and y in range(y2, y2 + h2):
                        num_of_screen = 3
            if num_of_screen == 2: # Экран начать игру
                x1, y1, w1, h1, x2, y2, w2, h2, x3, y3, w3, h3, x4, y4, w4, h4, x5, y5, w5, h5 = draw_start_game(screen)
                if event.key == pygame.K_ESCAPE:
                    num_of_screen = 1

            if num_of_screen == 3: # Экран как играть
                draw_how_to_play(screen)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        num_of_screen = 1

        pygame.display.flip()

    pygame.quit()