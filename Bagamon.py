import pygame
import random
from enum import Enum
import time
from sys import exit
pygame.init()

pygame.display.set_caption('Backgammon')
screen = pygame.display.set_mode((1280, 660))
pygame.display.set_icon(pygame.image.load('graphics/one.png'))

dice_state = {1:pygame.image.load('graphics/one.png'),
              2:pygame.image.load('graphics/two.png'),
              3:pygame.image.load('graphics/three.png'),
              4:pygame.image.load('graphics/four.png'),
              5:pygame.image.load('graphics/five.png'),
              6:pygame.image.load('graphics/six.png')}

dice_state_red = {1:pygame.image.load('Graphics/one_red.png'),
              2:pygame.image.load('graphics/two_red.png'),
              3:pygame.image.load('graphics/three_red.png'),
              4:pygame.image.load('graphics/four_red.png'),
              5:pygame.image.load('graphics/five_red.png'),
              6:pygame.image.load('graphics/six_red.png')}

Board = pygame.image.load('graphics/Board.png')
black_pikka = pygame.image.load('graphics/black_pika.png')
white_pikka = pygame.image.load('graphics/white_pika.png')

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
        self.random_x = random.randint(20,80)
        self.random_y = random.randint(120,260)
        self.random_x_red = random.randint(50,120)
        self.random_y_red = random.randint(300,450)
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
        self.cube_a = None
        self.cube_b = None
        self.cell_selected = None
        self.target_cell_a = None
        self.target_cell_b = None
        self.max_black_pikka = 15
        self.max_white_pikka = 15

    def switch_player(self):
        if self.player == PlayerColor.PLAYER_A:
            self.player = PlayerColor.PLAYER_B
        else:
           self.player = PlayerColor.PLAYER_A
        self.GameState = GameState.BEFORE_DICE_ROLL

    def starting_pos(self):
        for i in range(2):
            self.jail.append(Cell(PlayerColor.EMPTY, amount=0, x=0, y=0, right_x=0, left_x=0, bottom_y=0, top_y=0))
        self.jail[0] = Cell(PlayerColor.PLAYER_B, amount=0, x=1229, y=35, right_x=1260, left_x=1195, bottom_y=270, top_y=25)
        self.jail[1] = Cell(PlayerColor.PLAYER_A, amount=0, x=1229, y=582, right_x=1260, left_x=1195, bottom_y=635, top_y=392)

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
        if self.cube_a and self.cube_b != None:
            screen.blit(dice_state[self.cube_a.value], (self.cube_a.random_x, self.cube_a.random_y))
            screen.blit(dice_state_red[self.cube_b.value], (self.cube_b.random_x_red, self.cube_b.random_y_red))
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
                for d in range(jail.amount):
                    screen.blit(pikka, (pikka_rect.x, pikka_rect.y + space * d))

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
                for d in range(cell.amount):
                    screen.blit(pikka, (pikka_rect.x, pikka_rect.y + space * d))

            if cell.PlayerColor == PlayerColor.PLAYER_B:
                pikka = white_pikka
                pikka_rect = pikka.get_rect(midtop=(cell.x, cell.y))
                for d in range(cell.amount):
                    screen.blit(pikka, (pikka_rect.x, pikka_rect.y + space * d))
        self.gamelogic()

    def are_there_more_dice(self):
        if self.cube_a.is_available and self.cube_b.is_available:
            pass
        else:
            return False

    def is_there_someone_in_jail(self):
        if self.player == PlayerColor.PLAYER_A:
            if self.jail[0].amount > 0:
                pass
            else:
                return False
        if self.player == PlayerColor.PLAYER_B:
            if self.jail[1].amount > 0:
                pass
            else:
                return False

    def any_available_cell_free_jail(self):
        if self.player == PlayerColor.PLAYER_A:
            if self.board[self.cube_a.value].amount < 2:
                return True
            elif self.board[self.cube_b.value].amount < 2:
                return
        else:
            if self.board[23 - self.cube_a.value].amount < 2:
                return True
            elif self.board[23 - self.cube_b.value].amount < 2:
                return True
            else:
                return False

    def dice_roll(self):
        for i in pygame.event.get():
            if i.type == pygame.MOUSEBUTTONDOWN:
                mouse_poos = pygame.mouse.get_pos()
                if 3 < mouse_poos[0] < 205 and 90 < mouse_poos[1] < 575:
                    self.cube_a = Cube()
                    self.cube_b = Cube()
                    return self.cube_a, self.cube_b

    def is_home_full(self):
        if self.player == PlayerColor.PLAYER_A:

            if self.board[0].amount + self.board[1].amount + self.board[2].amount + self.board[3].amount + self.board[4].amount + self.board[5].amount == self.max_black_pikka:
                 return True
            else:
                return False
        else:
            if self.board[18].amount + self.board[1].amount + self.board[20].amount + self.board[21].amount + self.board[22].amount + self.board[23].amount == self.max_white_pikka:
                return True
            else:
                return False

    def condition_check(self):
        print(f'condition check {self.GameState}')
        if self.are_there_more_dice():
            if self.is_there_someone_in_jail():
                if self.any_available_cell_free_jail():
                    self.GameState = GameState.JAIL
                else:
                    self.switch_player()
            else:
                if self.is_home_full():
                    self.GameState = GameState.HOME_FULL
                else:
                    self.GameState = GameState.MOVEMENT_1

        else:
            self.switch_player()

    def cell_selection(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for cell_i, cell in enumerate(self.board):
                    if cell.left_x < mouse_pos[0] < cell.right_x and cell.top_y < mouse_pos[1] < cell.bottom_y:
                        self.selected_cell = cell_i
                        print(f'selected cell = {self.selected_cell}')
                        return True

    def is_selected_cell_valid(self):
        print(f'selected cell color {self.board[self.selected_cell].PlayerColor}')
        if self.board[self.selected_cell].PlayerColor == self.player:
            return True
        else:
            return False

    def is_target_cell_valid_a(self):
        if self.player == PlayerColor.PLAYER_A:
            if self.selected_cell + self.cube_a.value > 23:
                print('over_limit')
            else:
                self.target_cell_a = self.selected_cell + self.cube_a.value
                if self.board[self.selected_cell + self.cube_a.value].PlayerColor == self.player:
                    print('your color')
                    print(f'target cell a = {self.selected_cell + self.cube_a.value}')
                    return True

                elif self.board[self.selected_cell + self.cube_a.value].PlayerColor != self.player and \
                        self.board[self.selected_cell + self.cube_a.value].amount <= 1:
                    print('empty or 1 white')
                    print(f'target cell a = {self.selected_cell + self.cube_a.value}')
                    return True
                else:
                    print('cant move there')
                    print(f'target cell a = {self.selected_cell + self.cube_a.value}')
                    return False

        if self.player == PlayerColor.PLAYER_B:
            if self.selected_cell - self.cube_a.value < 0:
                print('over_limit')
            else:
                self.target_cell_a = self.selected_cell - self.cube_a.value
                if self.board[self.selected_cell - self.cube_a.value].PlayerColor == self.player:
                    print('your color')
                    print(f'target cell a = {self.selected_cell - self.cube_a.value}')
                    return True

                elif self.board[self.selected_cell - self.cube_a.value].PlayerColor != self.player and \
                        self.board[self.selected_cell - self.cube_a.value].amount <= 1:
                    print('empty or 1 black')
                    print(f'target cell a = {self.selected_cell - self.cube_a.value}')
                    return True
                else:
                    print('cant move there')
                    print(f'target cell a = {self.selected_cell - self.cube_a.value}')
                    return False

    def is_target_cell_valid_b(self):
        if self.player == PlayerColor.PLAYER_A:
            self.target_cell_b = self.selected_cell + self.cube_b.value
            if self.selected_cell + self.cube_b.value > 23:
                print('over_limit')
            else:
                if self.board[self.selected_cell + self.cube_b.value].PlayerColor == self.player:
                    print('your color')
                    print(f' target cell b = {self.selected_cell + self.cube_b.value}')
                    return True

                elif self.board[self.selected_cell + self.cube_b.value].PlayerColor != self.player and \
                        self.board[self.selected_cell + self.cube_b.value].amount <= 1:
                    print('empty or 1 white')
                    print(f' target cell b = {self.selected_cell + self.cube_b.value}')
                    return True

                else:
                    print('cant move there')
                    print(f' target cell b = {self.selected_cell + self.cube_b.value}')
                    return False

        if self.player == PlayerColor.PLAYER_B:
            self.target_cell_b = self.selected_cell - self.cube_b.value
            if self.selected_cell - self.cube_b.value < 0:
                print('over_limit')
            else:
                if self.board[self.selected_cell - self.cube_b.value].PlayerColor == self.player:
                    print('your color')
                    print(f' target cell b = {self.selected_cell - self.cube_b.value}')
                    return True

                elif self.board[self.selected_cell - self.cube_b.value].PlayerColor != self.player and \
                        self.board[self.selected_cell - self.cube_b.value].amount <= 1:
                    print('empty or 1 black')
                    print(f' target cell b = {self.selected_cell - self.cube_b.value}')
                    return True

                else:
                    print('cant move there')
                    print(f' target cell b = {self.selected_cell - self.cube_b.value}')
                    return False

    def select_target_a(self):
        if self.player == PlayerColor.PLAYER_A:
            if self.cell_selection():
                 if self.cell_selected == self.target_cell_a:
                     if self.board[self.selected_cell + self.cube_a.value].PlayerColor == self.player:
                         self.board[self.target_cell_a].amount -= 1
                         self.board[self.cell_selected].amount += 1
                         self.board[self.cell_selected].PlayerColor = self.player
                     elif self.board[self.selected_cell + self.cube_a.value].PlayerColor == PlayerColor.PLAYER_B and \
                                self.board[self.selected_cell + self.cube_a.value].amount <= 1:
                         self.board[self.target_cell_a].amount -= 1
                         self.board[self.cell_selected].PlayerColor = self.player
                     elif self.board[self.selected_cell + self.cube_a.value].PlayerColor == PlayerColor.EMPTY:
                         self.board[self.target_cell_a].amount -= 1
                         self.board[self.cell_selected].amount += 1
                         self.board[self.cell_selected].PlayerColor = self.player
                 else:
                     pass

        elif self.player == PlayerColor.PLAYER_B:
            if self.cell_selection():
                if self.cell_selected == self.target_cell_a:
                    if self.board[self.selected_cell - self.cube_a.value].PlayerColor == self.player:
                        self.board[self.target_cell_a].amount -= 1
                        self.board[self.cell_selected].amount += 1
                        self.board[self.cell_selected].PlayerColor = self.player
                    elif self.board[self.selected_cell - self.cube_a.value].PlayerColor == PlayerColor.PLAYER_B and \
                            self.board[self.selected_cell - self.cube_a.value].amount <= 1:
                        self.board[self.target_cell_a].amount -= 1
                        self.board[self.cell_selected].PlayerColor = self.player
                    elif self.board[self.selected_cell - self.cube_a.value].PlayerColor == PlayerColor.EMPTY:
                        self.board[self.target_cell_a].amount -= 1
                        self.board[self.cell_selected].amount += 1
                        self.board[self.cell_selected].PlayerColor = self.player

    def select_target_b(self):
        if self.player == PlayerColor.PLAYER_A:
            if self.cell_selected == self.target_cell_b:
                if self.board[self.selected_cell + self.cube_b.value].PlayerColor == self.player:
                    self.board[self.target_cell_b].amount -= 1
                    self.board[self.cell_selected].amount += 1
                    self.board[self.cell_selected].PlayerColor = self.player
                elif self.board[self.selected_cell + self.cube_b.value].PlayerColor == PlayerColor.PLAYER_B and \
                        self.board[self.selected_cell + self.cube_b.value].amount <= 1:
                    self.board[self.target_cell_a].amount -= 1
                    self.board[self.cell_selected].PlayerColor = self.player
                elif self.board[self.selected_cell + self.cube_b.value].PlayerColor == PlayerColor.EMPTY:
                    self.board[self.target_cell_b].amount -= 1
                    self.board[self.cell_selected].amount += 1
                    self.board[self.cell_selected].PlayerColor = self.player

        if self.player == PlayerColor.PLAYER_B:
            if self.cell_selected == self.target_cell_b:
                if self.board[self.selected_cell - self.cube_b.value].PlayerColor == self.player:
                    self.board[self.target_cell_b].amount -= 1
                    self.board[self.cell_selected].amount += 1
                    self.board[self.cell_selected].PlayerColor = self.player
                elif self.board[self.selected_cell - self.cube_b.value].PlayerColor == PlayerColor.PLAYER_B and \
                        self.board[self.selected_cell - self.cube_b.value].amount <= 1:
                    self.board[self.target_cell_a].amount -= 1
                    self.board[self.cell_selected].PlayerColor = self.player
                elif self.board[self.selected_cell - self.cube_b.value].PlayerColor == PlayerColor.EMPTY:
                    self.board[self.target_cell_b].amount -= 1
                    self.board[self.cell_selected].amount += 1
                    self.board[self.cell_selected].PlayerColor = self.player
            else:
                print('work')


    def gamelogic(self):
        if GameState.BEFORE_DICE_ROLL:
            self.dice_roll()
            if self.cell_selection():
                if self.is_selected_cell_valid():
                    if self.is_target_cell_valid_a() or self.is_target_cell_valid_b():
                        self.GameState = GameState.MOVEMENT_2
                    else:
                        self.GameState = GameState.MOVEMENT_1

                else:
                    print('not yours')

        elif GameState.MOVEMENT_1:
            print("movement")
            if self.cell_selection():
                print("cell selection")
                if self.is_selected_cell_valid():
                    print("is valid")
                    if self.is_target_cell_valid_a() or self.is_target_cell_valid_b():
                        self.GameState = GameState.MOVEMENT_2
                    else:
                        self.GameState = GameState.MOVEMENT_1

                else:
                    print('not yours')
        elif GameState.MOVEMENT_2:
            print('oko')
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