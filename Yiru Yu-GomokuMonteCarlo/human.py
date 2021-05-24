import pygame
from pygame.locals import *
from sys import exit
from ui import UI

import pygame
from pygame.locals import *



class Human(object):
    def __init__(self, board, player):
        self.board = board
        self.player = player
        
    def get_action(self):
        move = -1
        for event in pygame.event.get():            
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Human move")
                x,y = pygame.mouse.get_pos()
                print(x, y)
                if self.board.x_coord_min - self.board.space / 2 <= x <= self.board.x_coord_max + self.board.space / 2 and self.board.y_coord_min - self.board.space / 2 <= y <= self.board.y_coord_max + self.board.space / 2:              
                    h = self.board.height - int(round((y - self.board.y_coord_min) / self.board.space)) - 1
                    w = int(round((x - self.board.x_coord_min) / self.board.space))      
                    print(h, w)
                    try:                                                                    
                        #UI._instance.graphic(self.board, human, ai)
                        location = [h, w]
                        print(location)
                        move = self.board.location_to_move(location)
                       
                        '''
                        location = [int(n, 10) for n in input("your move: ").split(",")]
                        move = self.board.location_to_move(location)
                        '''
                    except Exception as e:
                        move = -1
                    if move == -1 or move not in self.board.availables:
                        print("invalid move: ")
                        move = self.get_action()
                    else:
                        break      
                
        return move
  
    def __str__(self):
        return "Human"