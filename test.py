import sys
import pygame
import random
from enum import Enum
from sys import exit
from pygame.locals import *
from pynput import *

pygame.init()
pygame.display.set_caption('Backgammon')
screen = pygame.display.set_mode((1280, 660))
Board = pygame.image.load('Graphics/WhatsApp Image 2023-03-28 at 14.13.04.jpeg')
black_pikka = pygame.image.load('Graphics/black_pika.png')
white_pikka = pygame.image.load('Graphics/white_pika.png')


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)


class PlayerColor(Enum):
    EMPTY = 0
    PLAYER_A = (0, 0, 0)
    PLAYER_B = (255, 255, 255)

class GameState(Enum):
    BEFORE_DICE_ROLL = 1
    AFTER_DICE_ROLL = 2
    AFTER_HOME_SELECTED = 3
    IN_JAIL = 4
    HOME_FULL = 5


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
def is_equal(yakov, rachel):
    return yakov.value == rachel.value

def movement():
    pass

class GameManager:
    def __init__(self):
        self.board = []
        self.jail = []
        self.player = PlayerColor.PLAYER_A
        self.running = True
        self.GameState = GameState.BEFORE_DICE_ROLL
        self.cube_a = Cube()
        self.cube_b = Cube()
        if is_equal(self.cube_a, self.cube_b):
            self.cube_a.set_double()
            self.cube_b.set_double()

    def switchplayer(self):
        if self.player == PlayerColor.PLAYER_A:
           self.player = PlayerColor.PLAYER_B
        else:
           self.player = PlayerColor.PLAYER_A

    def start(self):
        for i in range(2):
            self.jail.append(Cell(PlayerColor.EMPTY, 0, 0, 0, 0, 0, 0, 0))
        self.jail[0] = Cell(PlayerColor.PLAYER_B, 0, 143, 60, 297, 7, 126, 8)
        self.jail[1] = Cell(PlayerColor.PLAYER_A, 0, 145, 577, 292, 6, 518, 640)
        for i in range(24):
            self.board.append(Cell(PlayerColor.EMPTY, 0, 0, 0, 0, 0, 0, 0))
        self.board[0] = Cell(PlayerColor.PLAYER_A, amount=2, x=1230, y=10, right_x=1263, left_x=1200, bottom_y=334, top_y=8)
        self.board[5] = Cell(PlayerColor.PLAYER_B, 5, 835, 10, 875, 795, 327, 8)
        self.board[7] = Cell(PlayerColor.PLAYER_B, 3, 670, 10, 713, 630, 327, 8)
        self.board[11] = Cell(PlayerColor.PLAYER_A, 5, 345, 10, 390, 310, 327, 8)
        self.board[12] = Cell(PlayerColor.PLAYER_B, 5, 340, 590, 377, 303, 640, 331)
        self.board[16] = Cell(PlayerColor.PLAYER_A, 3, 655, 590, 688, 622, 640, 331)
        self.board[18] = Cell(PlayerColor.PLAYER_A, 5, 816, 590, 851, 781, 640, 331)
        self.board[23] = Cell(PlayerColor.PLAYER_B, 2, 1225, 590, 1267, 1185, 640, 331)

    def rendergame(self):
        screen.blit(Board, (0, 0))
        for cell_i, cell in enumerate(self.board):
            if cell.amount <= 5:
                space = 64
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
                        self.board[cell_i +1].amount += 1
                        self.board[cell_i + 1].PlayerColor = cell.PlayerColor
                    #    target_cell = cell_i =+ 1



    def gamelogic(self):
        if GameState.BEFORE_DICE_ROLL:
            pass
        elif GameState.AFTER_DICE_ROLL:
            pass
        elif GameState.AFTER_HOME_SELECTED:
            pass
        elif GameState.IN_JAIL:
            pass
        elif GameState.HOME_FULL:
            pass

    def run(self):
        self.start()
        while self.running:
            self.rendergame()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     self.running = False
                #if event.type == pygame.MOUSEBUTTONDOWN:
                    #mouse_pos = pygame.mouse.get_pos()
                   # print(mouse_pos)

game_manager = GameManager()
game_manager.run()
