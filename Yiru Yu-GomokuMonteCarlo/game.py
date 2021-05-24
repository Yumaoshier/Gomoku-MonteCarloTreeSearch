import numpy as np
import random
import pygame
from pygame.locals import *
import sys

from montecarlo import MCTS
from human import Human
from ui import UI


class Game(object):
    def __init__(self, board, **kwargs):
        self.board = board
        self.players = [1,2]
        self.time = float(kwargs.get("time", 5))
        self.max_actions = int(kwargs.get("max_actions", 1000))
        self.num_to_win = int(kwargs.get("num_to_win", 5))
        self.use_strategy = int(kwargs.get("use_strategy", True))
        #self.start = False
        self.is_beginning = True
    
    def init_player(self):
        plist = list(range(len(self.players)))
        index1 = np.random.choice(plist)
        plist.remove(index1)
        index2 = np.random.choice(plist)
        return self.players[index1], self.players[index2]
    
    def game_end(self, ai):
        win, winner = ai.get_winner(self.board)
        if win:
            return True, winner
        elif not len(self.board.availables):
            print("Game End")
            return True, -1
        return False, -1
    
    
    def show_end_ui(self, text):
        button_sets = UI._instance.show_end(text)
        clicked_restart = False
        result = None
        while(not clicked_restart and result is None):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()    
                clicked_restart, result = UI._instance.register_ui_restart_event(event)       
                UI._instance.register_ui_end_event(event)    
            for btn in button_sets:
                btn.draw()
            pygame.display.update()
        return clicked_restart, result
    
    def show_ui(self, p1, p2):
        button_sets = UI._instance.restart(p1, p2, self.board)
        clicked_start = False
        result = None
        while(not clicked_start and result is None):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()    
                clicked_start, result = UI._instance.register_ui_start_event(event)           
            for btn in button_sets:
                btn.draw()
            pygame.display.update()
        pygame.display.update()
        return clicked_start, result
    
    def set_info_text(self, p1_id, p1, p2_id, p2, cp):
        UI._instance.set_info_text(p1_id, p1, p2_id, p2, cp)
    
    def update_curInfo_text(self, cp):
        UI._instance.update_cur_text(cp)
  
    
    def start(self):
        if not self.is_beginning:
            return
        self.is_beginning = False
        
        p1, p2 = self.init_player()
        self.board.init_board()
        
        clicked, result = self.show_ui(p1, p2)
 
        ai = MCTS(self.board, [p1, p2], self.time, self.max_actions, self.num_to_win, self.use_strategy)
        human = Human(self.board, p2)
        players = {}
        players[p1] = ai
        players[p2] = human   
        self.set_info_text(p1, "AI", p2, "You", "")
        turn = [p1, p2]
        random.shuffle(turn)
        end_text = ""
        while(1):
            p = turn.pop(0)
            turn.append(p)
            player_in_turn = players[p]
            if player_in_turn == ai:
                self.update_curInfo_text("AI")
            else:
                self.update_curInfo_text("You")
            
            move = player_in_turn.get_action()       
            while(move < 0):                      
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()           
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.is_beginning = True
                            self.start()
                move = player_in_turn.get_action()
            
            self.board.update(p, move)
            #UI._instance.graphic(self.board, human, ai)       
            UI._instance.draw_pieces(p, move)
            end, winner = self.game_end(ai)
            if end:
                
                if winner != -1:
                    end_text = "GAME OVER,%s is win!" % players[winner]
                    print("Game End. Winner is ", players[winner])
                else:
                    end_text = "Game End. There is no Winner"
                    print("Game End. There is no Winner")
                #UI._instance.show_end(end_text)
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()           
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.is_beginning = True
                        self.start()
            
            
            pygame.display.update()
        
        clicked_restart, reuslt = self.show_end_ui(end_text)
        print(clicked_restart, reuslt)
        pygame.display.update()
        if clicked_restart and reuslt:
            self.is_beginning = True
            self.start()
        else:
            pygame.quit()
            sys.exit()   
         
        
       


                
                
                
            

            
    
            