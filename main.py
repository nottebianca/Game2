import pygame
import sys
import os


pygame.init()


WIDTH, HEIGHT = 1000, 500
WINDOW_SIZE = (WIDTH, HEIGHT)
WINDOW_TITLE = 'Pizza Simulator'
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


IMG_DIR = os.path.join(os.path.dirname(__file__), 'img')
MENU_IMG = pygame.image.load(os.path.join(IMG_DIR, 'menu.png'))


pizza_recipes = {
    "Пепперони": ["Тесто", "Томатный соус", "Пепперони", "Сыр"],
    "Гавайская": ["Тесто", "Томатный соус", "Ветчина", "Ананас", "Сыр"],
    "Маргарита": ["Тесто", "Томатный соус", "Помидоры", "Базилик", "Сыр"],
}

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None, *args):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = pygame.font.SysFont(None, 40)
        self.action = action
        self.args = args

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self.drawText(screen, self.text)

    def drawText(self, screen, text):
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and self.action:
                self.action(*self.args)

def quit_game():
    pygame.quit()
    sys.exit()

def choose_recipe_screen(screen):
    screen.fill(WHITE)
    pygame.display.set_caption("Выберите рецепт пиццы")

    recipe_buttons = []
    button_width = 200
    button_height = 50
    button_spacing = 20
    x = (WIDTH - button_width) // 2
    y = 100

    # Создание кнопок для каждого рецепта
    for index, (recipe_name, _) in enumerate(pizza_recipes.items()):
        button = Button(x, y, button_width, button_height, recipe_name, GREEN, WHITE, select_recipe, recipe_name, screen)
        recipe_buttons.append(button)
        y += button_height + button_spacing
    choosing = True
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in recipe_buttons:
                button.handleEvent(event)

        # Отображение кнопок
        for button in recipe_buttons:
            button.draw(screen)

        pygame.display.flip()

# Функция для обработки выбора рецепта
def select_recipe(recipe, screen):
    print("Выбран рецепт:", recipe)

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_TITLE)


play_button = Button(400, 250, 200, 50, 'Play', GREEN, WHITE, choose_recipe_screen, screen)
exit_button = Button(400, 320, 200, 50, 'Exit', RED, WHITE, quit_game)

clock = pygame.time.Clock()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        play_button.handleEvent(event)
        exit_button.handleEvent(event)
    screen.fill(WHITE)
    screen.blit(MENU_IMG, (0, 0))
    play_button.draw(screen)
    exit_button.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
sys.exit()