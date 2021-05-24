import pygame
from pygame.locals import *
from button import UIButton
from sys import exit

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
red = (255, 0, 0)

class UI(object):
    _instance = None
    
    def __init__(self):
        raise RuntimeError('Call instance() to initialize')
     
    @classmethod
    def instance(cls):
        if cls._instance is None:
            print("Creating UI instance")
            cls._instance = cls.__new__(cls)
            
        return cls._instance
    
    
    def initialize(self, board, background, white, black, screen, font):           
        self.screen = screen
        self.background = background
        #self.font = font
        self.white = white
        self.black = black       
        self.board = board
        self.dot_list = [(board.x_coord_min + j * board.space - self.white.get_width()/2, board.y_coord_max - i * board.space) for i in range(board.width) for j in range(board.height)]
        #print(self.dot_list)
        self.button_start = None
        self.button_end = None
        self.button_restart = None
        self.font = pygame.font.SysFont('Arial Rounded MT Bold',24)
        self.white_player_text = None
        self.black_player_text = None
        self.cur_player_text = None
        
    def set_font(self, font_name = 'Arial Rounded MT Bold', size = 28):
        self.font = pygame.font.SysFont(font_name, size)
        
    def set_info_text(self, p1, player1, p2, player2, cp, color = white):      
        if self.pieces_image[p1] == self.white:
            white_text = "White Player: " + player1
            black_text = "Black Player: " + player2
        else:
            white_text = "White Player: " + player2
            black_text = "Black Player: " + player1
            
        self.white_player_text = self.font.render(white_text, True, color)
        rect = self.white_player_text.get_rect()
        rect.center = (250, 10)
        self.screen.blit(self.white_player_text, rect)
        
        self.black_player_text = self.font.render(black_text, True, color)
        rect = self.black_player_text.get_rect()
        rect.center = (250, 30)
        self.screen.blit(self.black_player_text, rect)
                  
        cur_text = "Current Player: " + cp
        self.cur_player_text = self.font.render(cur_text, True, color)
        rect = self.cur_player_text.get_rect()
        rect.center = (250, 50)
        self.screen.blit(self.cur_player_text, rect)
        pygame.display.update()
            
            
    def update_cur_text(self, text = "", color = white):
        rect = self.cur_player_text.get_rect()
        rect.center = (250, 50)
        self.screen.fill(black, rect)
        cur_text = "Current Player: " + text
        self.cur_player_text = self.font.render(cur_text, True, color)
        rect = self.cur_player_text.get_rect()
        rect.center = (250, 50)       
        self.screen.blit(self.cur_player_text, rect)
        pygame.display.update()
       
        
        
    def restart(self, p1, p2, board):
        self.screen.blit(self.background, (65, 65))
        w = (self.board.width) * self.board.space
        h = (self.board.height) * self.board.space
        rect = self.background.get_rect().size       
        x = (rect[0] - w) / 2
        y = (rect[1] - h) / 2
        pygame.draw.rect(self.background, black, [x, y, w, h], 3)
        button_sets = self.show_ui_start()
        self.pieces_image = {}
        self.pieces_image[p1] = self.white
        self.pieces_image[p2] = self.black
        pygame.event.set_blocked([1,4,KEYUP,JOYAXISMOTION,JOYBALLMOTION,JOYBUTTONDOWN,JOYBUTTONUP,JOYHATMOTION])
        pygame.event.set_allowed([MOUSEBUTTONDOWN,MOUSEBUTTONUP,12,KEYDOWN])
        self.dot_list = [(board.x_coord_min + j * board.space - self.white.get_width()/2, 
                          board.y_coord_max - i * board.space) 
                         for i in range(board.width) for j in range(board.height)]
        pygame.display.flip()
        pygame.display.update()
        return button_sets
    
    def enter_game(self):
        self.screen.fill(black)
        self.screen.blit(self.background, (65, 65))
        
  
    def draw_pieces(self, player, move):        
        piece = self.pieces_image[player]
        self.screen.blit(piece, self.dot_list[move])
        print(move)
        print(self.dot_list[move])
        
    def show_end(self, text):
        end_text = self.font.render(text, True, red)
        rect = end_text.get_rect()
        rect.center = (250, 200)
        self.screen.blit(end_text, rect)
        if self.button_restart is None:
            self.button_restart = UIButton(self.screen, (170, 230, 160, 40))
            self.button_restart.text = "Restart"
            self.button_restart.click = self.click_restart_button
        elif not self.button_restart.visible:
            self.button_restart.visible = True
        
        if self.button_end is None:
            self.button_end = UIButton(self.screen, (170, 275, 160, 40))
            self.button_end.text = "Quit"
            self.button_end.click = self.click_end_button
        elif not self.button_end.visible:
            self.button_end.visible = True
            
        pygame.event.set_blocked(
            [1, 4, KEYUP, JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP,
             JOYHATMOTION,MOUSEBUTTONDOWN,MOUSEBUTTONUP])
        pygame.event.set_allowed(QUIT)
        
        return {self.button_restart, self.button_end}
        
        
    def show_ui_start(self):
        if self.button_start is None:
            self.button_start = UIButton(self.screen, (170, 230, 160, 40))
            self.button_start.text = "Start"
            self.button_start.click = self.click_start_button
        elif not self.button_start.visible:
            self.button_start.visible = True
        
        return {self.button_start}
 
    def click_start_button(self, btn):        
        btn.visible = False
        self.enter_game()   
        return True
    
    def click_restart_button(self, btn):
        btn.visible = False
        self.button_end.visible = False
        print("restart")
        self.enter_game()
        return True
    
    def click_end_button(self, btn):
        pygame.quit()
        exit()    
    
    def register_ui_restart_event(self, event):
       
        clicked, result = self.button_restart.update(event)
        return clicked, result
    
    def register_ui_start_event(self, event):
        clicked, result = self.button_start.update(event)
        return clicked, result
    
    def register_ui_end_event(self, event):
        self.button_end.update(event)
        
   
    def graphic(self, board, human, ai):     
  
        width = board.width
        height = board.height
 
        print("Human Player", human.player, "with X".rjust(3))
        print("AI    Player", ai.to_play, "with O".rjust(3))
        print()
        for x in range(width):
            print("{0:8}".format(x), end='')
        print('\r\n')
        for i in range(height - 1, -1, -1):
            print("{0:4d}".format(i), end='')
            for j in range(width):
                loc = i * width + j
                if board.states[loc] == human.player:
                    print('X'.center(8), end='')
                elif board.states[loc] == ai.to_play:
                    print('O'.center(8), end='')
                else:
                    print('_'.center(8), end='')
            print('\r\n\r\n')