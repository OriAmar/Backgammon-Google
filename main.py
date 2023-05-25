import pygame
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
        self.max_black_pikka = 15
        self.max_white_pikka = 15
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
        self.gamelogic()

    def movement(self):
        if self.cube_a.value == self.cube_b.value:
            self.cube_a.set_double()
            self.cube_b.set_double()
        print(self.cube_a.value, self.cube_b.value)
        print(self.cube_a.available, self.cube_b.available)
        for cell_i, cell in enumerate(self.board):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if cell.amount > 0:
                        if cell.left_x < mouse_pos[0] < cell.right_x and cell.top_y < mouse_pos[1] < cell.bottom_y:
                            if self.cube_a.is_available():
                                #for i in range(self.cube_a.available):
                                if self.board[cell_i + self.cube_a.value].PlayerColor == PlayerColor.EMPTY or self.board[cell_i + self.cube_a.value].PlayerColor == cell.PlayerColor:
                                    cell.amount -= 1
                                    if self.player.PLAYER_B:
                                        self.board[cell_i - self.cube_a.value].amount += 1
                                        self.board[cell_i + self.cube_a.value].PlayerColor = cell.PlayerColor
                                        self.cube_a.use()
                                    else:
                                        self.board[cell_i + self.cube_a.value].amount += 1
                                        self.board[cell_i + self.cube_a.value].PlayerColor = cell.PlayerColor
                                        self.cube_a.use()
                            elif self.cube_b.is_available():
                                #for i in range(self.cube_b.available):
                                if self.board[cell_i + self.cube_b.value].PlayerColor == PlayerColor.EMPTY or self.board[cell_i + self.cube_b.value].PlayerColor == cell.PlayerColor:
                                    cell.amount -= 1
                                    if self.player.PLAYER_B:
                                        self.board[cell_i - self.cube_a.value].amount += 1
                                        self.board[cell_i + self.cube_a.value].PlayerColor = cell.PlayerColor
                                        self.cube_a.use()
                                    else:
                                        self.board[cell_i + self.cube_a.value].amount += 1
                                        self.board[cell_i + self.cube_a.value].PlayerColor = cell.PlayerColor
                                        self.cube_a.use()
                            else:
                                self.switch_player()
                    else:
                        self.movement()
    def condition_check(self):
        if self.Are_there_more_dice():
            if self.Is_there_someone_in_jail():
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
    def Are_there_more_dice(self):
        if self.cube_a.is_available() and self.cube_b.is_available():
            return True
        else:
            return False
    def Is_there_someone_in_jail(self):
        if self.player == PlayerColor.PLAYER_A:
            if self.jail[1].amount > 0:
                return True
            else:
                return False
        else:
            if self.jail[0].amount > 0:
                return True
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


    def cell_home_selection(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for cell_i, cell in enumerate(self.board):
                    if cell.left_x < mouse_pos[0] < cell.right_x and cell.top_y < mouse_pos[1] < cell.bottom_y and self.player == cell.PlayerColor:
                        cell.amount -= 1
                        if self.board[cell_i + self.cube_a.value].PlayerColor == cell.PlayerColor:

                            return True
                    else:
                        return False
    def cell_target_selection(self, cell_i):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for cell_i, cell in enumerate(self.board):
                    if cell.left_x < mouse_pos[0] < cell.right_x and cell.top_y < mouse_pos[1] < cell.bottom_y and self.player == cell.PlayerColor:
                        return True
                    elif cell.left_x < mouse_pos[0] < cell.right_x and cell.top_y < mouse_pos[1] < cell.bottom_y and self.player != cell.PlayerColor:
                        return False

    def is_valid_target(self):
        for c_i in enumerate(self.board):
            if self.board[c_i + self.cube_a.value].PlayerColor == self.player or self.board[c_i + self.cube_a.value].PlayerColor :
                return True
            if self.board[c_i + self.cube_a.value].PlayerColor == self.player:
                return True
    def movement_first (self):
        if self.cell_selection():
            if self.is_valid_target():
                gamestate == movement2
            else:
                mo
        else:
            self.movement1()
    def gamelogic(self):
        if GameState.BEFORE_DICE_ROLL:
            print(self.cube_a.value, self.cube_b.value)
            print(self.cube_a.available, self.cube_b.available)
            if not self.cube_a.is_available() and not self.cube_b.is_available():
                self.switch_player()
            else:
                for c_i, c in enumerate(self.board):
                    if self.player.PLAYER_A:
                        print("שלום")
                        if self.jail[1].amount == 0:
                            print("כלא")
                            if self.board[c_i < 6].amount == 15 and self.board[c_i < 6].PlayerColor == PlayerColor.PLAYER_A:
                                #לשנות גיים סטייט ל- בית מלא
                                self.GameState = GameState.HOME_FULL
                                print("בית מלא")
                            else:
                                print("שמנה גיים")
                                self.GameState = GameState.MOVEMENT_1
                                break
                        else:
                            # שחרור
                            if self.cube_a.value or self.cube_b.value:
                                pass
                            else:
                                self.switch_player()
                    else:
                        if self.jail[0].amount == 0:
                            if self.board[c_i < 17].amount == 15 and self.board[c_i < 17].PlayerColor == PlayerColor.PLAYER_B:
                                #לשנות גיים סטייט ל- הזזה ראשונה
                                self.GameState = GameState.HOME_FULL
                            else:
                                self.GameState = GameState.MOVEMENT_1
                        else:
                            #שחרור
                            pass

        elif GameState.MOVEMENT_1:
            print("עובד")
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