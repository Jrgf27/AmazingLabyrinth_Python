class movements:
    def __init__(self):
        self.player=1
        self.board=[]
        self.extra_piece=[0,0,0,0]
        self.score=[0,0,0,0]
        self.move_player=False

class game_parameters:
    def __init__(self):
        self.player=0
        self.number_of_pieces=1
        self.board_pos=[]
        self.board_size=0
        self.extra_piece_pos=[]
        self.square_size=0

class server_info:
    def __init__(self):
        self.connections=[]
        self.player_number=1
        self.game_number=0
        self.game_info=[]
        self.new_moves=[]