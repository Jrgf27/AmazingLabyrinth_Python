import socket
import pickle

class Network():
    def __init__(self,total_players):
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server="192.168.1.79"
        # self.port=5555
        if total_players == 2:
            self.port=5555
        elif total_players == 3:
            self.port=5556
        elif total_players == 4:
            self.port=5557
        self.addr=(self.server,self.port)      
        self.player,self.number_of_pieces,self.board_pos,self.board_size,self.extra_piece_pos,self.square_size=self.connect()

    def getID(self):
        return self.id
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass
    
    def send(self,data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print (e)