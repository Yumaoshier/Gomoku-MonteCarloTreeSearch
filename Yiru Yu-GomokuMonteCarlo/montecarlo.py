import numpy as np
import math
import time
import copy

 

class MCTS:
    def __init__(self, board, players, time = 5, max_actions = 1000, num_to_win = 5, use_strategy = True):
        self.board = board
        self.visit_count = 0
        self.players = players     
        self.calculate_time = float(time)
        self.max_actions = max_actions
        
        self.to_play = players[0]
        self.coefficient = 1.96
        self.plays = {}
        self.wins = {}
        self.max_depth = 1
        self.num_to_win = num_to_win
        self.use_strategy = use_strategy
        
 
    
    def get_action(self):
        if len(self.board.availables) == 1:
            return self.board.availables[0]
        
        self.plays = {}
        self.win = {}
        simulations = 0
        begin = time.time()
        while time.time() - begin < self.calculate_time:
            board_copy = copy.deepcopy(self.board)
            turn_copy = copy.deepcopy(self.players)
            self.simulate(board_copy, turn_copy)
            simulations += 1
            
        print("total smulations: ", simulations)
        
        move = self.select_best_move()
        location = self.board.move_to_location(move)
        print("maximum depth searched: ", self.max_depth)
        print("AI move: %d,%d\n" % (location[0], location[1]))
        return move
      
        
    def expand(self, depth, player, move):
        self.plays[(player, move)] = 0
        self.wins[(player, move)] = 0
        if(depth > self.max_depth):
            self.max_depth = depth
    
    def backup(self, player, move, visited, winner):
        for (player, move) in visited:
            if (player, move) not in self.plays:
                continue
            self.plays[(player, move)] += 1
            if player == winner:
                self.wins[(player, move)] += 1
        
    
    def ucb_score(self, player, move, availables, log):
        cur_win_prob = self.wins[(player, move)] / self.plays[(player, move)]
        all_simu_prob = math.sqrt(self.coefficient * log / self.plays[(player, move)])
        return cur_win_prob + all_simu_prob
    
    def simulate(self, board, players):
        plays = self.plays
        #wins = self.wins
        availables = board.availables
        #print("original: ", availables)
        
        
        player = self.get_player(players)
        visited_states = set()
        winner = -1
        expand = True
        
        for t in range(1, self.max_actions + 1): 
            '''
            if self.use_strategy:
                adjacents = self.get_strategy_moves(board, players, plays)
                if len(adjacents) and len(adjacents) > 0:
                    availables = adjacents
                else:
                    availables = board.availables
            '''
                    #print("adjacents: ", availables)
            #print("availables: ", availables)
            if all(plays.get((player, move)) for move in availables):
                log_total = math.log(sum(plays[(player, move)] for move in availables))
                value, move = max((self.ucb_score(player, move, availables, log_total), move)
                                  for move in availables)
                #print("ucb move: ", move)
                
            else:
                if self.use_strategy:
                    move = self.strategy_move(board, player, plays)
                else:
                    move = np.random.choice(availables)
    
           # print("move: ", move)
            board.update(player, move)
            
            if expand and (player, move) not in plays:
                expand = False
                self.expand(t, player, move)
            
            visited_states.add((player, move))
            
            is_full = len(availables) == 0
            win, winner = self.get_winner(board)
            if is_full or win:
                break
            player = self.get_player(players)
        
        self.backup(player, move, visited_states, winner)
            
            
    def get_player(self, players):
        p = players.pop(0)
        players.append(p)
        return p
    
    def get_winner(self, board):
        moved = list(set(range(board.width * board.height)) - set(board.availables))
        if(len(moved) < self.num_to_win + 2):
            return False, -1
        
        width = board.width
        height = board.height
        states = board.states
        for m in moved:
            x = m // width
            y = m % width
            player = states[m]
            
            if(y in range(width - self.num_to_win + 1) and len(set(states[i] for i in range(m, m + self.num_to_win))) == 1):
                return True, player
            
            if(x in range(height - self.num_to_win + 1) and len(set(states[i] for i in range(m, m + self.num_to_win * width, width))) == 1):
                return True, player
            
            if(y in range(width - self.num_to_win + 1) and x in range(height - self.num_to_win + 1) and 
               len(set(states[i] for i in range(m, m + self.num_to_win * (width + 1), width + 1))) == 1):
                return True, player
            
            if(y in range(self.num_to_win - 1, width) and x in range(height - self.num_to_win + 1) and 
               len(set(states[i] for i in range(m, m + self.num_to_win * (width - 1), width -1))) == 1):
                return True, player
            
        return False, -1
    
    
    def select_best_move(self):
        precent_wins, move = max((self.wins.get((self.to_play, move), 0) / 
                                  self.plays.get((self.to_play, move), 1), 
                                 move) for move in self.board.availables)
        return move
    
    def get_strategy_moves(self, board, players, plays):
        adjacents = set()
        if len(board.availables) > self.num_to_win:            
            for p in players:
                adjacents = adjacents | set(self.adjacent_move(board, p, plays))           
            #adjacents = self.adjacent_move(board, player, plays)
        adjacents = list(adjacents)       
        return adjacents
    
    def strategy_move(self, board, player, plays):
        adjacents = []
        move = -1
        if len(board.availables) > self.num_to_win:
            adjacents = self.adjacent_move(board, player, plays)
        if len(adjacents):
            move = np.random.choice(adjacents)
        else:
            peripherals = []
            for move in board.availables:
                if not plays.get((player, move)):
                    peripherals.append(move)
            move = np.random.choice(peripherals)
        return move
    
    def adjacent_move(self, board, player, plays):
        width = board.width
        height = board.height
        moved = list(set(range(width * height)) - set(board.availables))
        #print("moved: ", moved)
        adjacents = set()
        for m in moved:
            r = m // width
            c = m % width
            if c < width - 1:      #right
                adjacents.add(m + 1)
            if r < height - 1:      #up
                adjacents.add(m + width)
            if c > 0:               #left
                adjacents.add(m - 1)
            if r > 0:                #down
                adjacents.add(m - width)
            if c < width - 1 and r < height - 1:   #right up
                adjacents.add(m + width + 1)
            if c < width - 1 and r > 0:            #right down
                adjacents.add(m - width + 1)
            if c > 0 and r < height - 1:           #left up
                adjacents.add(m + width - 1)
            if c > 0 and r > 0:                    # left down
                adjacents.add(m - width - 1)
        
        adjacents = list(set(adjacents) - set(moved))
        for move in adjacents:
            if plays.get((player, move)):
                adjacents.remove(move)
        return adjacents
    
    def __str__(self):
        return "AI"
    
    
            
            