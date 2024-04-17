import pygame
import sys
import os

# Инициализация Pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)  # Розовый

# Новый шрифт для кнопок
font = pygame.font.SysFont(None, 50)


# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.clicked = False
        self.hovered = False
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color if self.hovered else GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 3)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked = True
            return True
        return False

    def update(self, pos):
        if self.rect.collidepoint(pos):
            self.hovered = True
        else:
            self.hovered = False


def load_image(filename):
    return pygame.image.load(os.path.join("img", filename)).convert_alpha()


def draw_game_map(surface, color):
    # Очистим экран
    surface.fill(color)

    # Нарисуем стены
    wall_color = BLACK
    wall_thickness = 6
    wall_rects = [
        pygame.Rect(50, 50, 500, wall_thickness),
        pygame.Rect(50, 50, wall_thickness, 500),
        pygame.Rect(550 - wall_thickness, 50, wall_thickness, 500),
        pygame.Rect(50, 550 - wall_thickness, 500, wall_thickness),
        # Дополнительные стены или лабиринт можно нарисовать по вашему усмотрению
    ]
    for wall_rect in wall_rects:
        pygame.draw.rect(surface, wall_color, wall_rect)

    # Нарисуем точки
    dot_color = WHITE
    dot_radius = 3
    dot_positions = [
        (100, 100), (200, 100), (300, 100), (400, 100),
        (100, 200), (200, 200), (300, 200), (400, 200),
        (100, 300), (200, 300), (300, 300), (400, 300),
        (100, 400), (200, 400), (300, 400), (400, 400),
        # Дополнительные точки можно расставить по вашему усмотрению
    ]
    for dot_pos in dot_positions:
        pygame.draw.circle(surface, dot_color, dot_pos, dot_radius)


def draw_map(color):
    screen.fill(color)
    pygame.display.flip()


def game_screen(color):
    screen.fill(color)
    draw_game_map(screen, color)
    pygame.display.flip()
    print("Game started with color:", color)


def main():
    # Создание кнопок
    start_button = Button(200, 300, 200, 50, "Start", GREEN)
    top_scores_button = Button(200, 400, 200, 50, "Top scores", YELLOW)
    exit_button = Button(200, 500, 200, 50, "Exit", RED)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(pygame.mouse.get_pos()):
                    print("Start button clicked")
                    # Создание кнопок "Pink" и "Blue" после нажатия кнопки "Start"
                    blue_map_button = Button(200, 200, 100, 50, "Blue", BLUE)
                    pink_map_button = Button(310, 200, 100, 50, "Pink", PINK)
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if blue_map_button.is_clicked(pygame.mouse.get_pos()):
                                    print("Blue map selected")
                                    game_screen(BLUE)
                                    break
                                elif pink_map_button.is_clicked(pygame.mouse.get_pos()):
                                    print("Pink map selected")
                                    game_screen(PINK)
                                    break
                        blue_map_button.update(pygame.mouse.get_pos())
                        pink_map_button.update(pygame.mouse.get_pos())
                        screen.fill(WHITE)
                        screen.blit(menu_background, (0, 0))
                        blue_map_button.draw(screen)
                        pink_map_button.draw(screen)
                        pygame.display.flip()
                elif top_scores_button.is_clicked(pygame.mouse.get_pos()):
                    print("Top scores button clicked")
                elif exit_button.is_clicked(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
        start_button.update(pygame.mouse.get_pos())
        top_scores_button.update(pygame.mouse.get_pos())
        exit_button.update(pygame.mouse.get_pos())

        screen.fill(WHITE)
        screen.blit(menu_background, (0, 0))
        start_button.draw(screen)
        top_scores_button.draw(screen)
        exit_button.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman Menu")
    menu_background = load_image("main_menu3.jpg")
    main()
