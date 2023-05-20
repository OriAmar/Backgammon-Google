import pygame
import random
from enum import Enum
from sys import exit
pygame.init()

pygame.display.set_caption('Backgammon')
screen = pygame.display.set_mode((1200, 660))
pygame.display.set_icon(pygame.image.load('Graphics/one.png'))

dice_state = {1:pygame.image.load('graphics/one.png'),
              2:pygame.image.load('graphics/two.png'),
              3:pygame.image.load('graphics/three.png'),
              4:pygame.image.load('graphics/four.png'),
              5:pygame.image.load('graphics/five.png'),
              6:pygame.image.load('graphics/six.png')}

dice_state_red = {1:pygame.image.load('Graphics/graphics/one.png'),
              2:pygame.image.load('graphics/two_red.png'),
              3:pygame.image.load('graphics/three_red.png'),
              4:pygame.image.load('graphics/four_red.png'),
              5:pygame.image.load('graphics/five_red.png'),
              6:pygame.image.load('graphics/six_red.png')}

Board = pygame.image.load('graphics/board.png')
black_pikka = pygame.image.load('graphics/black_pika.png')
white_pikka = pygame.image.load('graphics/white_pika.png')
button = pygame.image.load('graphics/button.png')
button_rect = button.get_rect(topleft=(170,135))
button_pressed = pygame.image.load('graphics/button_pressed.png')
button_pressed_rect = button_pressed.get_rect(topleft=(128,0))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class PlayerColor(Enum):
    EMPTY = 0
    PLAYER_A = (0,0,0)
    PLAYER_B = (255, 255, 255)

class GameState(Enum):
    BEFORE_DICE_ROLL = 1
    MOVEMENT_1 = 2
    MOVEMENT_2 = 3
    JAIL = 4
    HOME_FULL = 5
    VICTORY = 6

class Cube:
    def __init__(self):
        self.value = random.randint(1, 6)
        self.available = 1
    def is_available(self):
        return self.available >= 1
    def use(self):
        self.available -= 1
    def set_double(self):
        self.available = 2
def is_equal(DICE1, DICE2):
        return DICE1.value == DICE2.value

def movement():
    pass

class Cell:
    def __init__(self, PlayerColor, amount, x, y, right_x, left_x, bottom_y, top_y):
        self.PlayerColor = PlayerColor
        self.amount = amount
        self.x = x
        self.y = y
        self.right_x = right_x
        self.left_x = left_x
        self.bottom_y = bottom_y
        self.top_y = top_y

    def is_empty(self):
        return self.PlayerColor == PlayerColor.EMPTY

class GameManager:
    def __init__(self):
        self.jail = []
        self.board = []
        self.player = PlayerColor.PLAYER_A
        self.running = True
        self.GameState = GameState.BEFORE_DICE_ROLL
        self.cube_a = Cube()
        self.cube_b = Cube()
        if is_equal(self.cube_a, self.cube_b):
            self.cube_a.set_double()
            self.cube_b.set_double()

    def switch_player(self):
        if self.player == PlayerColor.PLAYER_A:
            self.player = PlayerColor.PLAYER_B
        else:
           self.player = PlayerColor.PLAYER_A

    def starting_pos(self):

        for i in range(2):
            self.jail.append(Cell(PlayerColor.EMPTY, amount=0, x=0, y=0, right_x=0, left_x=0, bottom_y=0, top_y=0))
        self.jail[0] = Cell(PlayerColor.PLAYER_B, amount=0, x=143, y=60, right_x=297, left_x=7, bottom_y=126, top_y=8)
        self.jail[1] = Cell(PlayerColor.PLAYER_A, amount=0, x=145, y=577, right_x=292, left_x=6, bottom_y=518, top_y=640)

        for i in range(24):
            self.board.append(Cell(PlayerColor.EMPTY, amount=0, x=0, y=0, right_x=0, left_x=0, bottom_y=0, top_y=0))
        self.board[0] = Cell(PlayerColor.PLAYER_A, amount=2, x=1055, y=25, right_x=1263, left_x=1200, bottom_y=295, top_y=15)
        self.board[1] = Cell(PlayerColor.EMPTY, amount=0, x=987, y=25, right_x=1090, left_x=1020, bottom_y=295, top_y=15)
        self.board[2] = Cell(PlayerColor.EMPTY, amount=0, x=919, y=25, right_x=1020, left_x=950, bottom_y=295, top_y=15)
        self.board[3] = Cell(PlayerColor.EMPTY, amount=0, x=851, y=25, right_x=950, left_x=880, bottom_y=295, top_y=15)
        self.board[4] = Cell(PlayerColor.EMPTY, amount=0, x=783, y=25, right_x=880, left_x=810, bottom_y=295, top_y=15)
        self.board[5] = Cell(PlayerColor.PLAYER_B, amount=5, x=717, y=25, right_x=810, left_x=740, bottom_y=295, top_y=15)
        self.board[6] = Cell(PlayerColor.EMPTY, amount=0, x=600, y=25, right_x=0, left_x=0, bottom_y=295, top_y=15)
        self.board[7] = Cell(PlayerColor.PLAYER_B, amount=3, x=532, y=25, right_x=0, left_x=0, bottom_y=295, top_y=15)
        self.board[8] = Cell(PlayerColor.EMPTY, amount=0, x=464, y=25, right_x=0, left_x=0, bottom_y=295, top_y=15)
        self.board[9] = Cell(PlayerColor.EMPTY, amount=0, x=396, y=25, right_x=0, left_x=0, bottom_y=295, top_y=15)
        self.board[10] = Cell(PlayerColor.EMPTY, amount=0, x=328, y=25, right_x=0, left_x=0, bottom_y=295, top_y=15)
        self.board[11] = Cell(PlayerColor.PLAYER_A, amount=5, x=260, y=25, right_x=0, left_x=0, bottom_y=295, top_y=15)
        self.board[12] = Cell(PlayerColor.PLAYER_B, amount=5, x=260, y=585, right_x=0, left_x=0, bottom_y=640, top_y=370)
        self.board[13] = Cell(PlayerColor.EMPTY, amount=0, x=328, y=585, right_x=0, left_x=0, bottom_y=640, top_y=370)
        self.board[14] = Cell(PlayerColor.EMPTY, amount=0, x=396, y=585, right_x=0, left_x=0, bottom_y=640, top_y=370)
        self.board[15] = Cell(PlayerColor.EMPTY, amount=0, x=464, y=585, right_x=0, left_x=0, bottom_y=640, top_y=370)
        self.board[16] = Cell(PlayerColor.PLAYER_A, amount=3, x=532, y=585, right_x=0, left_x=0, bottom_y=640, top_y=370)
        self.board[17] = Cell(PlayerColor.EMPTY, amount=0, x=600, y=585, right_x=0, left_x=0, bottom_y=640, top_y=370)
        self.board[18] = Cell(PlayerColor.PLAYER_A, amount=5, x=717, y=585, right_x=0, left_x=0, bottom_y=640, top_y=370)
        self.board[19] = Cell(PlayerColor.EMPTY, amount=0, x=783, y=585, right_x=0, left_x=0, bottom_y=640, top_y=370)
        self.board[20] = Cell(PlayerColor.EMPTY, amount=0, x=851, y=585, right_x=0, left_x=0, bottom_y=640, top_y=370)
        self.board[21] = Cell(PlayerColor.EMPTY, amount=0, x=919, y=585, right_x=0, left_x=0, bottom_y=640, top_y=370)
        self.board[22] = Cell(PlayerColor.EMPTY, amount=0, x=987, y=585, right_x=0, left_x=0, bottom_y=640, top_y=370)
        self.board[23] = Cell(PlayerColor.PLAYER_B, amount=2, x=1055, y=585, right_x=0, left_x=0, bottom_y=640, top_y=370)

    def render_game(self):
        screen.blit(Board, (0, 0))
        for cell_i, cell in enumerate(self.board):
            if cell.amount <= 5:
                space = 48

            else:
                space = 30

            if cell_i >= 12:
                space *= -1

            if cell.PlayerColor == PlayerColor.PLAYER_A:
                pikka = black_pikka
                pikka_rect = pikka.get_rect(midtop=(cell.x, cell.y))

            if cell.PlayerColor == PlayerColor.PLAYER_B:
                pikka = white_pikka
                pikka_rect = pikka.get_rect(midtop=(cell.x, cell.y))

            for d in range(cell.amount):
                screen.blit(pikka, (pikka_rect.x, pikka_rect.y + space * d))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if cell.left_x < mouse_pos[0] < cell.right_x and cell.top_y < mouse_pos[1] < cell.bottom_y:
                        cell.amount -= 1
                        self.board[cell_i + 1].amount += 1
                        self.board[cell_i + 1].PlayerColor = cell.PlayerColor
                     #   target_cell = cell_i =+ 1

    def gamelogic(self):
        if GameState.BEFORE_DICE_ROLL:
            pass
        elif GameState.MOVEMENT_1:
            pass
        elif GameState.MOVEMENT_2:
            pass
        elif GameState.JAIL:
            pass
        elif GameState.HOME_FULL:
            pass
        elif GameState.VICTORY:
            pass

    def run(self):
        self.starting_pos()
        while self.running:
            self.render_game()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:import pygame
import random
from enum import Enum
import time
from sys import exit
pygame.init()

pygame.display.set_caption('Backgammon')
screen = pygame.display.set_mode((1280, 660))
pygame.display.set_icon(pygame.image.load('Graphics/one.png'))

dice_state = {1:pygame.image.load('graphics/one.png'),
              2:pygame.image.load('graphics/two.png'),
              3:pygame.image.load('graphics/three.png'),
              4:pygame.image.load('graphics/four.png'),
              5:pygame.image.load('graphics/five.png'),
              6:pygame.image.load('graphics/six.png')}

dice_state_red = {1:pygame.image.load('Graphics/one.png'),
              2:pygame.image.load('graphics/two_red.png'),
              3:pygame.image.load('graphics/three_red.png'),
              4:pygame.image.load('graphics/four_red.png'),
              5:pygame.image.load('graphics/five_red.png'),
              6:pygame.image.load('graphics/six_red.png')}

Board = pygame.image.load('graphics/Board.png')
black_pikka = pygame.image.load('graphics/black_pika.png')
white_pikka = pygame.image.load('graphics/white_pika.png')
button = pygame.image.load('graphics/button.png')
button_rect = button.get_rect(topleft=(170,135))
button_pressed = pygame.image.load('graphics/button_pressed.png')
button_pressed_rect = button_pressed.get_rect(topleft=(128,0))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class PlayerColor(Enum):
    EMPTY = 0
    PLAYER_A = 1
    PLAYER_B = 2

class GameState(Enum):
    BEFORE_DICE_ROLL = 1
    MOVEMENT_1 = 2
    MOVEMENT_2 = 3
    JAIL = 4
    HOME_FULL = 5
    VICTORY = 6

class Cube:
    def __init__(self):
        self.value = random.randint(1, 6)
        self.available = 1
    def is_available(self):
        return self.available >= 1
    def use(self):
        self.available -= 1
    def set_double(self):
        self.available = 2
def is_equal(DICE1, DICE2):
        return DICE1.value == DICE2.value

class Cell:
    def __init__(self, PlayerColor, amount, x, y, right_x, left_x, bottom_y, top_y):
        self.PlayerColor = PlayerColor
        self.amount = amount
        self.x = x
        self.y = y
        self.right_x = right_x
        self.left_x = left_x
        self.bottom_y = bottom_y
        self.top_y = top_y

    def is_empty(self):
        return self.PlayerColor == PlayerColor.EMPTY

class GameManager:
    def __init__(self):
        self.jail = []
        self.board = []
        self.player = PlayerColor.PLAYER_A
        self.running = True
        self.GameState = GameState.BEFORE_DICE_ROLL
        self.cube_a = Cube()
        self.cube_b = Cube()

    def switch_player(self):
        if self.player == PlayerColor.PLAYER_A:
            self.player = PlayerColor.PLAYER_B
        else:
           self.player = PlayerColor.PLAYER_A

    def starting_pos(self):
        for i in range(2):
            self.jail.append(Cell(PlayerColor.EMPTY, amount=0, x=0, y=0, right_x=0, left_x=0, bottom_y=0, top_y=0))
        self.jail[0] = Cell(PlayerColor.PLAYER_B, amount=1, x=1229, y=35, right_x=1260, left_x=1195, bottom_y=270, top_y=25)
        self.jail[1] = Cell(PlayerColor.PLAYER_A, amount=1, x=1229, y=582, right_x=1260, left_x=1195, bottom_y=635, top_y=392)

        for i in range(24):
            self.board.append(Cell(PlayerColor.EMPTY, amount=0, x=0, y=0, right_x=0, left_x=0, bottom_y=0, top_y=0))
        self.board[0] = Cell(PlayerColor.PLAYER_A, amount=2, x=1133, y=25, right_x=1170, left_x=1095, bottom_y=320, top_y=23)
        self.board[1] = Cell(PlayerColor.EMPTY, amount=0, x=1056, y=25, right_x=1095, left_x=1022, bottom_y=320, top_y=23)
        self.board[2] = Cell(PlayerColor.EMPTY, amount=0, x=981, y=25, right_x=1022, left_x=947, bottom_y=320, top_y=23)
        self.board[3] = Cell(PlayerColor.EMPTY, amount=0, x=909, y=25, right_x=947, left_x=873, bottom_y=320, top_y=23)
        self.board[4] = Cell(PlayerColor.EMPTY, amount=0, x=834, y=25, right_x=873, left_x=800, bottom_y=320, top_y=23)
        self.board[5] = Cell(PlayerColor.PLAYER_B, amount=5, x=762, y=25, right_x=800, left_x=727, bottom_y=320, top_y=23)
        self.board[6] = Cell(PlayerColor.EMPTY, amount=0, x=634, y=25, right_x=672, left_x=597, bottom_y=320, top_y=23)
        self.board[7] = Cell(PlayerColor.PLAYER_B, amount=3, x=561, y=25, right_x=597, left_x=522, bottom_y=320, top_y=23)
        self.board[8] = Cell(PlayerColor.EMPTY, amount=0, x=486, y=25, right_x=522, left_x=448, bottom_y=320, top_y=23)
        self.board[9] = Cell(PlayerColor.EMPTY, amount=0, x=411, y=25, right_x=448, left_x=374, bottom_y=320, top_y=23)
        self.board[10] = Cell(PlayerColor.EMPTY, amount=0, x=336, y=25, right_x=374, left_x=303, bottom_y=320, top_y=23)
        self.board[11] = Cell(PlayerColor.PLAYER_A, amount=5, x=266, y=25, right_x=303, left_x=225, bottom_y=320, top_y=23)
        self.board[12] = Cell(PlayerColor.PLAYER_B, amount=5, x=266, y=585, right_x=303, left_x=225, bottom_y=635, top_y=340)
        self.board[13] = Cell(PlayerColor.EMPTY, amount=0, x=335, y=585, right_x=374, left_x=303, bottom_y=635, top_y=340)
        self.board[14] = Cell(PlayerColor.EMPTY, amount=0, x=410, y=585, right_x=448, left_x=374, bottom_y=635, top_y=340)
        self.board[15] = Cell(PlayerColor.EMPTY, amount=0, x=484, y=585, right_x=522, left_x=448, bottom_y=635, top_y=340)
        self.board[16] = Cell(PlayerColor.PLAYER_A, amount=3, x=562, y=585, right_x=597, left_x=522, bottom_y=635, top_y=340)
        self.board[17] = Cell(PlayerColor.EMPTY, amount=0, x=631, y=585, right_x=672, left_x=597, bottom_y=635, top_y=340)
        self.board[18] = Cell(PlayerColor.PLAYER_A, amount=5, x=762, y=585, right_x=800, left_x=727, bottom_y=635, top_y=340)
        self.board[19] = Cell(PlayerColor.EMPTY, amount=0, x=834, y=585, right_x=873, left_x=800, bottom_y=635, top_y=340)
        self.board[20] = Cell(PlayerColor.EMPTY, amount=0, x=909, y=585, right_x=947, left_x=873, bottom_y=635, top_y=340)
        self.board[21] = Cell(PlayerColor.EMPTY, amount=0, x=983, y=585, right_x=1022, left_x=947, bottom_y=635, top_y=340)
        self.board[22] = Cell(PlayerColor.EMPTY, amount=0, x=1060, y=585, right_x=1095, left_x=1022, bottom_y=635, top_y=340)
        self.board[23] = Cell(PlayerColor.PLAYER_B, amount=2, x=1134, y=585, right_x=1170, left_x=1095, bottom_y=635, top_y=340)

    def rendergame(self):
        screen.blit(Board, (0, 0))
        for jail_i, jail in enumerate(self.jail):
            if jail.amount <= 5:
                space = 48

            else:
                space = 30

            if jail_i >= 1:
                space *= -1

            if jail.PlayerColor == PlayerColor.PLAYER_A:
                pikka = black_pikka
                pikka_rect = pikka.get_rect(midtop=(jail.x, jail.y))

            if jail.PlayerColor == PlayerColor.PLAYER_B:
                pikka = white_pikka
                pikka_rect = pikka.get_rect(midtop=(jail.x, jail.y))

            for d in range(jail.amount):
                screen.blit(pikka, (pikka_rect.x, pikka_rect.y + space * d))
        for cell_i, cell in enumerate(self.board):
            if cell.amount <= 5:
                space = 48

            else:
                space = 30

            if cell_i >= 12:
                space *= -1

            if cell.PlayerColor == PlayerColor.PLAYER_A:
                pikka = black_pikka
                pikka_rect = pikka.get_rect(midtop=(cell.x, cell.y))

            if cell.PlayerColor == PlayerColor.PLAYER_B:
                pikka = white_pikka
                pikka_rect = pikka.get_rect(midtop=(cell.x, cell.y))

            for d in range(cell.amount):
                screen.blit(pikka, (pikka_rect.x, pikka_rect.y + space * d))
        self.movement()

    def movement(self):
        if self.cube_a.value == self.cube_b.value:
            self.cube_a.set_double()
            self.cube_b.set_double()
        print(self.cube_a.value, self.cube_b.value)
        for cell_i, cell in enumerate(self.board):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if cell.amount > 0:
                        if cell.left_x < mouse_pos[0] < cell.right_x and cell.top_y < mouse_pos[1] < cell.bottom_y:
                            if self.cube_a.is_available():
                                for i in range(self.cube_a.available):
                                    if self.board[cell_i + self.cube_a.value].PlayerColor == PlayerColor.EMPTY or self.board[cell_i + self.cube_a.value].PlayerColor == cell.PlayerColor:
                                        cell.amount -= 1
                                        self.board[cell_i + self.cube_a.value].amount += 1
                                        self.board[cell_i + self.cube_a.value].PlayerColor = cell.PlayerColor
                                        self.cube_a.use()
                            elif self.cube_b.is_available():
                                for i in range(self.cube_b.available):
                                    if self.board[cell_i + self.cube_b.value].PlayerColor == PlayerColor.EMPTY or self.board[cell_i + self.cube_b.value].PlayerColor == cell.PlayerColor:
                                        cell.amount -= 1
                                        self.board[cell_i + self.cube_b.value].amount += 1
                                        self.board[cell_i + self.cube_b.value].PlayerColor = cell.PlayerColor
                                        self.cube_b.use()
                            else:
                                self.switch_player()
                    else:
                        self.movement()

    def gamelogic(self):
        if GameState.BEFORE_DICE_ROLL:

           print(self.cube_a.value, self.cube_b.value)

           if not self.cube_a.is_available() or not self.cube_b.is_available():
               self.switch_player()
           else:
               for prison in self.jail:
                   for c_i, c in enumerate(self.board):
                    if prison.amount == 0:
                        if c_i < 6 and c.amount >= 15 and self.player == PlayerColor.PLAYER_A:
                            #לשנות גיים סטייט ל- בית מלא
                            self.GameState = GameState.HOME_FULL
                        elif c_i > 17  and c.amount >= 15 and self.player == PlayerColor.PLAYER_B:
                            #לשנות גיים סטייט ל- הזזה ראשונה
                            self.GameState = GameState.HOME_FULL

                    else:
                        if self.cube_a.value or self.cube_b.value:
                            pass
                        else:
                            self.switch_player()

        elif GameState.MOVEMENT_1:
            print(self.cube_a.value, self.cube_b.value)
            for cell_i, cell in enumerate(self.board):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if cell.amount > 0:
                            if cell.left_x < mouse_pos[0] < cell.right_x and cell.top_y < mouse_pos[1] < cell.bottom_y:
                                if self.cube_a.is_available():
                                    for i in range(self.cube_a.available):
                                        if self.board[cell_i + self.cube_a.value].PlayerColor == PlayerColor.EMPTY or self.board[cell_i + self.cube_a.value].PlayerColor == cell.PlayerColor:
                                            cell.amount -= 1
                                            self.board[cell_i + self.cube_a.value].amount += 1
                                            self.board[cell_i + self.cube_a.value].PlayerColor = cell.PlayerColor
                                            self.cube_a.use()
                                elif self.cube_b.is_available():
                                    for i in range(self.cube_b.available):
                                        if self.board[cell_i + self.cube_b.value].PlayerColor == PlayerColor.EMPTY or self.board[cell_i + self.cube_b.value].PlayerColor == cell.PlayerColor:
                                            cell.amount -= 1
                                            self.board[cell_i + self.cube_b.value].amount += 1
                                            self.board[cell_i + self.cube_b.value].PlayerColor = cell.PlayerColor
                                            self.cube_b.use()
                                else:
                                    self.switch_player()
                        else:
                            self.movement()

        elif GameState.MOVEMENT_2:
            if self.cube_a.is_available() or self.cube_b.is_available():
                self.GameState = GameState.MOVEMENT_1
            else:
                self.switch_player()

        elif GameState.JAIL:
            pass

        elif GameState.HOME_FULL:
            for cell_i, cell in enumerate(self.board):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if cell.left_x < mouse_pos[0] < cell.right_x and cell.top_y < mouse_pos[1] < cell.bottom_y:

                            if self.player == PlayerColor.PLAYER_A:
                                player = -1
                            else:
                                player = 1

                            if self.cube_a.value or self.cube_b.value * player + self.board[cell_i] == 23 or 0:
                                cell.amount -= 1
                            else:
                                self.GameState = GameState.MOVEMENT_1
                            if self.player == PlayerColor.PLAYER_A and self.board[cell_i < 6].amount == 0:
                                self.GameState = GameState.VICTORY
                            elif self.player == PlayerColor.PLAYER_B and self.board[cell_i > 17].amount == 0:
                                self.GameState = GameState.VICTORY


        elif GameState.VICTORY:
            for cell in self.board:
                if self.board[cell].PlayerColor == PlayerColor.PLAYER_A and self.board[cell].amount == 0:
                    print("you won")
                    time.sleep(60)
                    self.running = False
                elif self.board[cell].PlayerColor == PlayerColor.PLAYER_A and self.board[cell].amount == 0:
                    print("your opponent won")
                    print("you won")
                    time.sleep(60)
                    self.running = False

    def run(self):
        self.starting_pos()
        while self.running:
            self.rendergame()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

game_manager = GameManager()
game_manager.run()
                    self.running = False

game_manager = GameManager()
game_manager.run()

