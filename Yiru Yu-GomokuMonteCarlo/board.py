

class Board(object):
    def __init__(self, width, height, num_to_win, size, edge0, edgeX, edgeY, space):
        self.width = width
        self.height = height
        self.size = size
        self.states = {}
        self.availables = 0
        self.num_to_win = num_to_win
        self.x_coord_min = edge0 + edgeX
        self.x_coord_max = size - edge0 - edgeX
        self.y_coord_min = edge0 + edgeX
        self.y_coord_max = size - edge0 - edgeY
        self.space = space
        
        
    def init_board(self):
        if self.width < self.num_to_win or self.height < self.num_to_win:
            raise Exception('board width and height can not be less than %d' % self.num_to_win)
            
        self.availables = list(range(self.width * self.height))
        for m in self.availables:
            self.states[m] = -1
            
    def move_to_location(self, move):
        x = move // self.width
        y = move % self.width
        return [x, y]
    
    
    
    def location_to_move(self, location):
        if len(location) < 2:
            return -1
        h = location[0]
        w = location[1]
        index = h * self.width + w
        if index not in range(self.width * self.height):
            return -1
        return index
    
    def update(self, player, move):
        self.states[move] = player
        #print("self.availavles: ", self.availables)
        self.availables.remove(move)
        