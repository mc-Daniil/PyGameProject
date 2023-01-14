import pygame


def draw_intro_screen(screen, i):
    font = pygame.font.Font(None, 40)
    texts = ["Приветствую", "Это моя игра", "В ней нужно сбежать от учителя"]
    if i < len(texts):
        screen.fill((0, 0, 0))
        text = font.render(str(texts[i]), True, (100, 255, 100))
        x = width // 2 - text.get_width() // 2
        y = height // 2 - text.get_height() // 2
        screen.blit(text, (x, y))
    else:
        global num_of_screen
        num_of_screen = 1


def draw_start_screen(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)

    text1 = font.render("Начать игру", True, (100, 255, 100))
    x1 = width // 2 - text1.get_width() // 2
    y1 = height // 2 - text1.get_height()
    w1 = text1.get_width()
    h1= text1.get_height()
    screen.blit(text1, (x1, y1))

    text2 = font.render("Как играть", True, (100, 255, 100))
    x2 = width // 2 - text2.get_width() // 2
    y2 = height // 2 + text2.get_height()
    w2 = text2.get_width()
    h2 = text2.get_height()
    screen.blit(text2, (x2, y2))

    pygame.draw.rect(screen, (0, 255, 0), (x1 - 5, y1 - 5, w1 + 10, h1 + 10), 1)
    pygame.draw.rect(screen, (0, 255, 0), (x2 - 5, y2 - 5, w2 + 10, h2 + 10), 1)

    return x1, y1, w1, h1, x2, y2, w2, h2


def draw_start_game(screen):
    screen.fill((0, 255, 0))


def draw_how_to_play(screen):
    screen.fill((255, 0, 0))


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1200, 800
    screen = pygame.display.set_mode(size)
    num_of_screen = 0
    num_start_screen = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if num_of_screen == 0:
                draw_intro_screen(screen, num_start_screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    num_start_screen += 1
            if num_of_screen == 1:
                x1, y1, w1, h1, x2, y2, w2, h2 = draw_start_screen(screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x in range(x1, x1 + w1) and y in range(y1, y1 + h1):
                        num_of_screen = 2
                    elif x in range(x2, x2 + w2) and y in range(y2, y2 + h2):
                        num_of_screen = 3
            if num_of_screen == 2:
                draw_start_game(screen)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        num_of_screen = 1
            if num_of_screen == 3:
                draw_how_to_play(screen)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        num_of_screen = 1


        pygame.display.flip()

    pygame.quit()