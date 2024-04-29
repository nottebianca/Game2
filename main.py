import random

import pygame
from pinky import Pinky, Pinky_directions
from blinky import Blinky, Blinky_directions
from inky import Inky, Inky_directions
from clyde import Clyde, Clyde_directions
import sys
from pygame.image import load
import sqlite3
conn = sqlite3.connect('top_scores.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS scores
             (score INTEGER)''')
conn.commit()


black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)
cherry_color = (3, 0, 0)
bright_blue = (0, 0, 255)


pygame.init()
screen = pygame.display.set_mode([606, 606])
pygame.display.set_caption('Pacman')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)
pack = pygame.image.load('img/packman.png')
pygame.display.set_icon(pack)
pygame.mixer.init()
pygame.mixer.music.load('music/menu_music.mp3')
pygame.mixer.music.play(-1, 0.0)
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
bright_green = (0, 255, 0)
bright_yellow = (255, 255, 0)
bright_red = (255, 0, 0)
def save_score(score):
    # Insert score into the database
    c.execute("INSERT INTO scores (score) VALUES (?)", (score,))
    conn.commit()


def load_scores():
    # Retrieve scores from the database and return as a list
    c.execute("SELECT score FROM scores ORDER BY score DESC")
    scores = c.fetchall()
    return [score[0] for score in scores]


def update_top_scores(score):
    # Load scores and check if the new score should be added
    scores = load_scores()
    if not scores or len(scores) < 5 or score > scores[-1]:
        save_score(score)
        show_notification("New top score achieved!")


def show_top_scores_screen(screen):
    scores = load_scores()
    background_image = pygame.image.load("img/top.jpg").convert()
    screen.blit(background_image, (0, 0))
    draw_text('Top Scores', font, white, screen, 220, 20)
    y = 70
    for i, score in enumerate(scores[:5], 1):
        if i == 1:
            color = (255, 215, 0)
        elif i == 2:
            color = (128, 128, 128)
        elif i == 3:
            color = (205, 127, 50)
        else:
            color = white
        draw_text(f"{i}. {score}", font, color, screen, 250, y)
        y += 30

    draw_text('Press ESC to return to main menu', font, white, screen, 150, 500)
    pygame.display.update()


def close_connection():
    conn.close()

def show_notification(message):
    print(message)
def start_game():
    print("Starting the game...")
    class Wall(pygame.sprite.Sprite):
        def __init__(self, x, y, width, height, color):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.top = y
            self.rect.left = x


    def setupRoomOne(all_sprites_list):
        wall_list = pygame.sprite.RenderPlain()
        walls = [[0, 0, 6, 600],
             [0, 0, 600, 6],
             [0, 600, 606, 6],
             [600, 0, 6, 606],
             [300, 0, 6, 66],
             [60, 60, 186, 6],
             [360, 60, 186, 6],
             [60, 120, 66, 6],
             [60, 120, 6, 126],
             [180, 120, 246, 6],
             [300, 120, 6, 66],
             [480, 120, 66, 6],
             [540, 120, 6, 126],
             [120, 180, 126, 6],
             [120, 180, 6, 126],
             [360, 180, 126, 6],
             [480, 180, 6, 126],
             [180, 240, 6, 126],
             [180, 360, 246, 6],
             [420, 240, 6, 126],
             [240, 240, 42, 6],
             [324, 240, 42, 6],
             [240, 240, 6, 66],
             [240, 300, 126, 6],
             [360, 240, 6, 66],
             [0, 300, 66, 6],
             [540, 300, 66, 6],
             [60, 360, 66, 6],
             [60, 360, 6, 186],
             [480, 360, 66, 6],
             [540, 360, 6, 186],
             [120, 420, 366, 6],
             [120, 420, 6, 66],
             [480, 420, 6, 66],
             [180, 480, 246, 6],
             [300, 480, 6, 66],
             [120, 540, 126, 6],
             [360, 540, 126, 6],
             ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], blue)
            wall_list.add(wall)
            all_sprites_list.add(wall)

        return wall_list


    def setupGate(all_sprites_list):
        gate = pygame.sprite.RenderPlain()
        gate.add(Wall(282, 242, 42, 2, white))
        all_sprites_list.add(gate)
        return gate


    class Block(pygame.sprite.Sprite):
        def __init__(self, color, width, height):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([width, height])
            self.image.fill(white)
            self.image.set_colorkey(white)
            pygame.draw.ellipse(self.image, color, [0, 0, width, height])
            self.rect = self.image.get_rect()


    class Player(pygame.sprite.Sprite):
        change_x = 0
        change_y = 0

        def __init__(self, x, y, filename):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(filename).convert()
            self.rect = self.image.get_rect()
            self.rect.top = y
            self.rect.left = x
            self.prev_x = x
            self.prev_y = y

        def prevdirection(self):
            self.prev_x = self.change_x
            self.prev_y = self.change_y

        def changespeed(self, x, y):
            self.change_x += x
            self.change_y += y

        def update(self, walls, gate):
            old_x = self.rect.left
            new_x = old_x + self.change_x
            prev_x = old_x + self.prev_x
            self.rect.left = new_x
            old_y = self.rect.top
            new_y = old_y + self.change_y
            prev_y = old_y + self.prev_y
            x_collide = pygame.sprite.spritecollide(self, walls, False)
            if x_collide:
                self.rect.left = old_x
            else:
                self.rect.top = new_y
                y_collide = pygame.sprite.spritecollide(self, walls, False)
                if y_collide:
                    self.rect.top = old_y
            if gate != False:
                gate_hit = pygame.sprite.spritecollide(self, gate, False)
                if gate_hit:
                    self.rect.left = old_x
                    self.rect.top = old_y


    class Ghost(Player):
        def changespeed(self, list, ghost, turn, steps, l):
            try:
                z = list[turn][2]
                if steps < z:
                    self.change_x = list[turn][0]
                    self.change_y = list[turn][1]
                    steps += 1
                else:
                    if turn < l:
                        turn += 1
                    elif ghost == "clyde":
                        turn = 2
                    else:
                        turn = 0
                    self.change_x = list[turn][0]
                    self.change_y = list[turn][1]
                    steps = 0
                return [turn, steps]
            except IndexError:
                return [0, 0]




    pl = len(Pinky_directions) - 1
    bl = len(Blinky_directions) - 1
    il = len(Inky_directions) - 1
    cl = len(Clyde_directions) - 1

    pygame.init()

    screen = pygame.display.set_mode([606, 606])

    pygame.display.set_caption('Pacman')

    background = pygame.Surface(screen.get_size())

    background = background.convert()

    background.fill(black)

    clock = pygame.time.Clock()

    pygame.font.init()
    font = pygame.font.Font("freesansbold.ttf", 24)

    w = 303 - 16
    p_h = (7 * 60) + 19
    m_h = (4 * 60) + 19
    b_h = (3 * 60) + 19
    i_w = 303 - 16 - 32
    c_w = 303 + (32 - 16)


    def startGame():
        all_sprites_list = pygame.sprite.RenderPlain()
        block_list = pygame.sprite.RenderPlain()
        monsta_list = pygame.sprite.RenderPlain()
        pacman_collide = pygame.sprite.RenderPlain()
        wall_list = setupRoomOne(all_sprites_list)
        gate = setupGate(all_sprites_list)
        p_turn = 0
        p_steps = 0
        b_turn = 0
        b_steps = 0
        i_turn = 0
        i_steps = 0
        c_turn = 0
        c_steps = 0
        Pacman = Player(w, p_h, "img/packman.png")
        all_sprites_list.add(Pacman)
        pacman_collide.add(Pacman)
        Blinky = Ghost(w, b_h, "img/blinky.png")
        monsta_list.add(Blinky)
        all_sprites_list.add(Blinky)
        Pinky = Ghost(w, m_h, "img/pinky.png")
        monsta_list.add(Pinky)
        all_sprites_list.add(Pinky)
        Inky = Ghost(i_w, m_h, "img/inky.png")
        monsta_list.add(Inky)
        all_sprites_list.add(Inky)
        Clyde = Ghost(c_w, m_h, "img/clyde.png")
        monsta_list.add(Clyde)
        all_sprites_list.add(Clyde)
        cherry_image = load('img/cherry_small.png').convert()
        cherry_image.set_colorkey(white)
        strawberry_image = pygame.image.load('img/strawberry_small.png').convert()
        strawberry_image.set_colorkey(white)

        # Вместо некоторых вишен, добавляем клубнику в случайно выбранные места
        if block_list:
            for _ in range(5):
                cherry = random.choice(block_list.sprites())  # Выбираем случайную вишню из списка
                cherry.rect.x = random.randint(0, 570)  # Случайная координата x
                cherry.rect.y = random.randint(0, 570)  # Случайная координата y
                cherry.image = strawberry_image  # Заменяем изображение на клубнику
        for row in range(19):
            for column in range(19):
                if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                    continue
                else:
                    # Проверяем, является ли текущая ячейка стеной
                    is_wall = any(
                        wall.rect.collidepoint((30 * column + 6) + 26, (30 * row + 6) + 26) for wall in wall_list)
                    if not is_wall:
                        # Создаем и добавляем клубнику только если текущая ячейка не является стеной
                        block = Block(cherry_color, 4, 4)
                        pygame.draw.ellipse(block.image, cherry_color, [0, 0, 606, 606])
                        block_image = pygame.transform.scale(strawberry_image, (10, 10))
                        block = Block(cherry_color, 10, 10)
                        block.image = block_image
                        block.rect = block_image.get_rect()
                        block.rect.x = (30 * column + 6) + 26
                        block.rect.y = (30 * row + 6) + 26
                        block_list.add(block)
                        all_sprites_list.add(block)

                    b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                    p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
                    if b_collide:
                        continue
                    elif p_collide:
                        continue
                    else:
                        # Add the block to the list of objects
                        block_list.add(block)
                        all_sprites_list.add(block)

        bll = len(block_list)
        score = 0
        done = False
        i = 0
        while done == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        Pacman.changespeed(-30, 0)
                    if event.key == pygame.K_RIGHT:
                        Pacman.changespeed(30, 0)
                    if event.key == pygame.K_UP:
                        Pacman.changespeed(0, -30)
                    if event.key == pygame.K_DOWN:
                        Pacman.changespeed(0, 30)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        Pacman.changespeed(30, 0)
                    if event.key == pygame.K_RIGHT:
                        Pacman.changespeed(-30, 0)
                    if event.key == pygame.K_UP:
                        Pacman.changespeed(0, 30)
                    if event.key == pygame.K_DOWN:
                        Pacman.changespeed(0, -30)
            Pacman.update(wall_list, gate)
            returned = Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
            p_turn = returned[0]
            p_steps = returned[1]
            Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
            Pinky.update(wall_list, False)
            returned = Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
            b_turn = returned[0]
            b_steps = returned[1]
            Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
            Blinky.update(wall_list, False)
            returned = Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
            i_turn = returned[0]
            i_steps = returned[1]
            Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
            Inky.update(wall_list, False)
            returned = Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
            c_turn = returned[0]
            c_steps = returned[1]
            Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
            Clyde.update(wall_list, False)
            blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
            if len(blocks_hit_list) > 0:
                score += len(blocks_hit_list)
            screen.fill(black)
            wall_list.draw(screen)
            gate.draw(screen)
            all_sprites_list.draw(screen)
            monsta_list.draw(screen)
            text = font.render("Score: " + str(score) + "/" + str(bll), True, red)
            screen.blit(text, [10, 10])
            if score == bll:
                update_top_scores(score)
                doNext("Congratulations, you won!", 145, all_sprites_list, block_list, monsta_list, pacman_collide,
                       wall_list, gate, score)
            monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)
            if monsta_hit_list:
                doNext("Game Over", 235, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate, score)
            pygame.display.flip()
            clock.tick(10)

    def doNext(message, left, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate, score):
        # Проверяем, установил ли игрок новый рекорд
        update_top_scores(score)
        top_scores = load_scores()
        new_record_index = -1

        # Проверяем, попал ли игрок в топ-5 и на какой позиции
        for i, top_score in enumerate(top_scores[:5]):  # Limit to top 5 scores
            if score >= top_score:
                new_record_index = i
                break

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if event.key == pygame.K_RETURN:
                        del all_sprites_list
                        del block_list
                        del monsta_list
                        del pacman_collide
                        del wall_list
                        del gate
                        startGame()

            w = pygame.Surface((400, 200))
            w.set_alpha(10)
            w.fill((128, 128, 128))
            screen.blit(w, (100, 200))
            text1 = font.render(message, True, white)
            screen.blit(text1, [left, 233])
            if new_record_index >= 0 and new_record_index < 5:
                text2 = font.render("            New top score!", True, white)
                screen.blit(text2, [135, 263])
                text3 = font.render(f"            You are now {new_record_index + 1}!", True, white)
                screen.blit(text3, [135, 293])
            else:
                text2 = font.render("   You are under top-5.", True, white)
                screen.blit(text2, [155, 263])

            text4 = font.render("To play again, press ENTER.", True, white)
            screen.blit(text4, [135, 323])
            text5 = font.render("To quit, press ESCAPE.", True, white)
            screen.blit(text5, [165, 353])
            pygame.display.flip()
            clock.tick(10)

    startGame()
def show_instructions(screen):
    background_image = pygame.image.load("img/instructions.jpg").convert()
    screen.blit(background_image, (0, 0))
    draw_text('Instructions', font, white, screen, 220, 200)
    instructions = [
        "Используйте стрелочки для передвижения.",
        "Съешьте все вишни для победы.",
        "При столкновении с врагом игра закончится.",
        "Нажмите ESC для выхода в главное меню."
    ]
    y = 250
    for instruction in instructions:
        draw_text(instruction, font, white, screen, 50, y)

        y += 30

    draw_text('Press ESC to return to main menu', font, white, screen, 150, 500)
    pygame.display.update()

def main_menu(screen):
    background_image = pygame.image.load("img/main_menu5.jpg").convert()

    while True:
        screen.blit(background_image, (0, 0))
        draw_text('Main menu', font, white, screen, 20, 20)

        play_button = pygame.Rect(200, 200, 200, 50)
        top_scores_button = pygame.Rect(200, 270, 200, 50)
        instructions_button = pygame.Rect(200, 340, 200, 50)
        exit_button = pygame.Rect(200, 410, 200, 50)

        mouse_pos = pygame.mouse.get_pos()
        play_highlighted = play_button.collidepoint(mouse_pos)
        top_scores_highlighted = top_scores_button.collidepoint(mouse_pos)
        instructions_highlighted = instructions_button.collidepoint(mouse_pos)
        exit_highlighted = exit_button.collidepoint(mouse_pos)

        play_color = bright_green if play_highlighted else green
        top_scores_color = bright_yellow if top_scores_highlighted else yellow
        instructions_color = bright_blue if instructions_highlighted else blue
        exit_color = bright_red if exit_highlighted else red

        pygame.draw.rect(screen, play_color, play_button)
        pygame.draw.rect(screen, top_scores_color, top_scores_button)
        pygame.draw.rect(screen, instructions_color, instructions_button)
        pygame.draw.rect(screen, exit_color, exit_button)

        draw_text('Start', font, black, screen, 270, 210)
        draw_text('Top scores', font, black, screen, 240, 280)
        draw_text('Instructions', font, black, screen, 240, 350)  # Центрируем по центру кнопки
        draw_text('Exit', font, black, screen, 270, 420)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse_pos):
                    start_game()
                elif top_scores_button.collidepoint(mouse_pos):
                    show_top_scores_screen(screen)
                    pygame.display.update()
                    wait_for_key()
                elif instructions_button.collidepoint(mouse_pos):
                    show_instructions(screen)
                    pygame.display.update()
                    wait_for_key()
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()




def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False



main_menu(screen)
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('Pacman')
    main_menu(screen)
    close_connection()
    pygame.quit()
