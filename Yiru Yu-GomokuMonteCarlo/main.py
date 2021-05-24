from ui import UI
from game import Game
from board import Board
import pygame
from pygame.locals import *
from sys import exit
import math

pygame.init()

board_image = "images/board.png"
white_image = "images/piece_white.png"
black_image = "images/piece_black.png"

original_width = 14
orihinal_height = 14
width = 8
height = 8

size = 500
space = 24
edge0 = 65
edgeX = 30 + (original_width - width) / 2 * space
edgeY = 40 + (orihinal_height - height) / 2 * space


screen = pygame.display.set_mode((size, size))
pygame.display.set_caption("GoMoKu MCTS - Yiru Yu")
background = pygame.image.load(board_image)
white = pygame.image.load(white_image).convert_alpha()
black = pygame.image.load(black_image).convert_alpha()

font = pygame.font.SysFont("black", 28)
pygame.event.set_blocked([1,4,KEYUP,JOYAXISMOTION,JOYBALLMOTION,JOYBUTTONDOWN,JOYBUTTONUP,JOYHATMOTION])
pygame.event.set_allowed([MOUSEBUTTONDOWN,MOUSEBUTTONUP,12,KEYDOWN])
'''
screen.blit(background, (65, 65))       
pygame.display.update()
'''


args = {
        "time": 5,
        "max_actions":1000,
        "num_to_win": 5,
        "use_strategy": True
        }

game_ui = UI.instance()
board = Board(width, height, int(args.get("num_to_win", 5)), size, edge0, edgeX, edgeY, space)
game_ui.initialize(board, background, white, black, screen, font)
game = Game(board, **args)
game.start()


        


