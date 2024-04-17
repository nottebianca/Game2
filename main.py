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


# Загрузка изображения
def load_image(filename):
    return pygame.image.load(os.path.join("img", filename)).convert_alpha()


# Основной игровой цикл
def main():
    # Загрузка изображения
    menu_image = load_image("main_menu3.jpg")

    # Создание кнопок
    start_button = Button(200, 300, 200, 50, "Start", GREEN)
    top_scores_button = Button(200, 400, 200, 50, "Top scores", YELLOW)
    exit_button = Button(200, 500, 200, 50, "Exit", RED)

    # Загрузка музыки
    pygame.mixer.music.load("music/menu_music.mp3")
    pygame.mixer.music.play(-1)  # -1 означает воспроизведение бесконечное количество раз

    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(pygame.mouse.get_pos()):
                    print("Start button clicked")
                elif top_scores_button.is_clicked(pygame.mouse.get_pos()):
                    print("Top scores button clicked")
                elif exit_button.is_clicked(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        # Обновление состояния кнопок
        start_button.update(pygame.mouse.get_pos())
        top_scores_button.update(pygame.mouse.get_pos())
        exit_button.update(pygame.mouse.get_pos())

        # Отрисовка
        screen.fill(WHITE)
        screen.blit(menu_image, (0, 0))  # Отображение изображения меню
        start_button.draw(screen)
        top_scores_button.draw(screen)
        exit_button.draw(screen)
        pygame.display.flip()


# Запуск игры
if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pacman Menu")
    main()
