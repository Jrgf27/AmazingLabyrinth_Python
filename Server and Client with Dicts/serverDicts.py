import socket
from _thread import *
from game_info import movements, game_parameters, server_info
import pickle
import random

########################################## Networking
server = "192.168.1.79"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

g=game_parameters()
server_info=server_info()
try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

########################################## Game Parameters

BOARD_NUMBER_PIECES=20
TOTAL_PLAYERS=2
NUMBER_OF_PIECES=[0,1,2,3]
NUMBER_OF_ROTATIONS=[0,1,2,3]
BOARD_POSITION=[150,150]
BOARD_PIXEL_SIZE=200
EXTRA_PIECE_POSITION=[250,800]

""" Each board piece has 4 parameters: [piece type, rotation of piece, player in piece, treasure in piece]
    Piece 0 is straight path, 1 is star, 2 is corner, 3 is T-junction; Rotation parameters coded into each piece generation code.
"""
"""movement -> board pieces are inserted with two coordinates (x,y) 
with x defining if piece is inserted vertically (0 bottom, 1 top) or horizontally (2 left, 3 right)
and y defining which collumn/row the piece is to be inserted into (index starting at 0)"""

#########################################

def initial_board_generator(BOARD_NUMBER_PIECES,NUMBER_OF_PIECES,NUMBER_OF_ROTATIONS,TOTAL_PLAYERS):
    m.board={}
    for i in range(BOARD_NUMBER_PIECES):
        for j in range (BOARD_NUMBER_PIECES):
            m.board[i,j]=[random.choice(NUMBER_OF_PIECES),random.choice(NUMBER_OF_ROTATIONS),0,0]

    if TOTAL_PLAYERS >= 1:
        m.board[0,0][0]=2
        m.board[0,0][1]=0
        m.board[0,0][2]=1
    if TOTAL_PLAYERS >=2:
        m.board[BOARD_NUMBER_PIECES-1,BOARD_NUMBER_PIECES-1][0]=2
        m.board[BOARD_NUMBER_PIECES-1,BOARD_NUMBER_PIECES-1][1]=2
        m.board[BOARD_NUMBER_PIECES-1,BOARD_NUMBER_PIECES-1][2]=2
    # if TOTAL_PLAYERS >=3:
    #     m.board[0][BOARD_NUMBER_PIECES-1][0]=2
    #     m.board[0][BOARD_NUMBER_PIECES-1][1]=3
    #     m.board[0][BOARD_NUMBER_PIECES-1][2]=3
    # if TOTAL_PLAYERS == 4:
    #     m.board[BOARD_NUMBER_PIECES-1][0][0]=2
    #     m.board[BOARD_NUMBER_PIECES-1][0][1]=1
    #     m.board[BOARD_NUMBER_PIECES-1][0][2]=4
    #     m.board[BOARD_NUMBER_PIECES-1][BOARD_NUMBER_PIECES-1][2]=2
    m.board[BOARD_NUMBER_PIECES//2,BOARD_NUMBER_PIECES//2][3]=1
    return m.board

def movingboard(piece=9,movement=None,board=None):
    vertical_lenght=horizontal_lenght=int(len(board)**0.5) #Number of collumns
    new_piece=piece
    #Vertical Movement
    if movement[0]==0: #Bottom to top   
        if board[0,movement[1]][2] != 0 or board[0,movement[1]][3] != 0:
            move_player=False
        else:
            new_piece=board[0,movement[1]]
            for i in range(0,vertical_lenght):
                if i == vertical_lenght-1:
                    board[i,movement[1]]=piece
                else:
                    board[i,movement[1]]=board[i+1,movement[1]]
            move_player=True     

    elif movement[0]==1: #Top to Bottom
        if board[vertical_lenght-1,movement[1]][2] != 0 or board[vertical_lenght-1,movement[1]][3]!= 0:
            move_player=False
        else:
            new_piece=board[vertical_lenght-1,movement[1]]
            for i in range(vertical_lenght-1,-1,-1):
                if i == 0:
                    board[i,movement[1]]=piece
                else:
                    board[i,movement[1]]=board[i-1,movement[1]]
            move_player=True

    #Horizontal Movement
    elif movement[0]==2: #Left to right
        if board[movement[1],horizontal_lenght-1][2] == 0 and board[movement[1],horizontal_lenght-1][3] == 0:
            new_piece=board[movement[1],horizontal_lenght-1]
            for i in range(horizontal_lenght-1,-1,-1):
                
                if i == 0:
                    board[movement[1],i]=piece
                else:
                    board[movement[1],i]=board[movement[1],i-1]
            
            move_player=True
        else:
            move_player=False
    elif movement[0]==3: #Right to left
        if board[movement[1],0][2] == 0 and board[movement[1],0][3] == 0:
            new_piece=board[movement[1],0]

            for i in range(vertical_lenght):
                if i == horizontal_lenght -1:
                    board[movement[1],i]=piece
                else:
                    board[movement[1],i]=board[movement[1],i+1]

            move_player=True
        else:
            move_player=False
    if not move_player:
        print("Invalid, player or treasure would be removed from board")
    return new_piece,move_player

def validity_board_generator(board):
    validity_board={}
    board_length=int(len(board)**0.5)
    for i in range(board_length):
        for j in range(board_length):
            ###### Straight Piece ##############
            if board[i,j][0]==0 and (board[i,j][1]==0 or board[i,j][1]==2):
                validity_board[i,j]=[0,1,0,1]
            elif board[i,j][0]==0 and (board[i,j][1]==1 or board[i,j][1]==3):
                validity_board[i,j]=[1,0,1,0]
            ###### Star Piece ####################
            elif board[i,j][0]==1:
                validity_board[i,j]=[1,1,1,1]
            ###### Corner Piece ####################
            elif board[i,j][0]==2 and board[i,j][1]==0:
                validity_board[i,j]=[0,0,1,1]
            elif board[i,j][0]==2 and board[i,j][1]==1:
                validity_board[i,j]=[0,1,1,0]
            elif board[i,j][0]==2 and board[i,j][1]==2:
                validity_board[i,j]=[1,1,0,0]
            elif board[i,j][0]==2 and board[i,j][1]==3:
                validity_board[i,j]=[1,0,0,1]
            ###### T-Junction Piece ################
            elif board[i,j][0]==3 and board[i,j][1]==0:
                validity_board[i,j]=[1,0,1,1]
            elif board[i,j][0]==3 and board[i,j][1]==1:
                validity_board[i,j]=[0,1,1,1]
            elif board[i,j][0]==3 and board[i,j][1]==2:
                validity_board[i,j]=[1,1,1,0]
            elif board[i,j][0]==3 and board[i,j][1]==3:
                validity_board[i,j]=[1,1,0,1]
    return validity_board

def extra_piece_insertion(move_player,extra_piece,board,mouse_x_position,mouse_y_position):

    if mouse_y_position==-1 and mouse_x_position<=BOARD_NUMBER_PIECES-1 and mouse_x_position>=0:
        extra_piece,move_player=movingboard(extra_piece,(1,mouse_x_position),board) 
    elif mouse_y_position==BOARD_NUMBER_PIECES and mouse_x_position<=BOARD_NUMBER_PIECES-1 and mouse_x_position>=0:
        extra_piece,move_player=movingboard(extra_piece,(0,mouse_x_position),board)
    elif mouse_x_position==-1 and mouse_y_position<=BOARD_NUMBER_PIECES-1 and mouse_y_position>=0:
        extra_piece,move_player=movingboard(extra_piece,(2,mouse_y_position),board)
    elif mouse_x_position==BOARD_NUMBER_PIECES and mouse_y_position<=BOARD_NUMBER_PIECES-1 and mouse_y_position>=0:
        extra_piece,move_player=movingboard(extra_piece,(3,mouse_y_position),board)
    else:
        print("Invalid, not clicking on appropriate places")
        return extra_piece, move_player

    return extra_piece, move_player

def move_validation(checking_board,input_direction,mouse_y_position,mouse_x_position,player_x_position,player_y_position):      
    valid_move=False
    input_direction_original=input_direction
    if mouse_y_position==player_y_position and mouse_x_position==player_x_position:
        return True
    if input_direction=="Right":
        pass
    else:
        if checking_board[player_y_position,player_x_position][0]==1 and player_x_position!=0:
            if checking_board[player_y_position,player_x_position-1][2]==1:
                checking_board[player_y_position,player_x_position][0]=0
                player_x_position-=1
                input_direction="Left"
                valid_move=move_validation(checking_board,input_direction,mouse_y_position,mouse_x_position,player_x_position,player_y_position)
                if valid_move:
                    return valid_move
                player_x_position+=1
                input_direction=input_direction_original
    if input_direction=="Down":
        pass
    else:    
        if checking_board[player_y_position,player_x_position][1]==1 and player_y_position != 0:
            if checking_board[player_y_position-1,player_x_position][3]==1:
                checking_board[player_y_position,player_x_position][1]=0
                player_y_position-=1
                input_direction="Up"
                valid_move=move_validation(checking_board,input_direction,mouse_y_position,mouse_x_position,player_x_position,player_y_position)
                if valid_move:
                    return valid_move
                player_y_position+=1
                input_direction=input_direction_original
    if input_direction == "Left":
        pass
    else:    
        if checking_board[player_y_position,player_x_position][2]==1 and player_x_position!=(int(len(checking_board)**0.5)-1):
            if checking_board[player_y_position,player_x_position+1][0]==1:
                checking_board[player_y_position,player_x_position][2]=0
                player_x_position+=1
                input_direction="Right"
                valid_move=move_validation(checking_board,input_direction,mouse_y_position,mouse_x_position,player_x_position,player_y_position)
                if valid_move:
                    return valid_move
                player_x_position-=1
                input_direction=input_direction_original
    
    if input_direction=="Up":
        pass
    else:
        if checking_board[player_y_position,player_x_position][3]==1 and player_y_position != (int(len(checking_board)**0.5)-1):
            if checking_board[player_y_position+1,player_x_position][1]==1:
                checking_board[player_y_position,player_x_position][3]=0
                player_y_position+=1
                input_direction="Down"
                valid_move=move_validation(checking_board,input_direction,mouse_y_position,mouse_x_position,player_x_position,player_y_position)
                if valid_move:
                    return valid_move
                player_y_position-=1
                input_direction=input_direction_original
    return valid_move

def threaded_client(conn, player,game_number):
        
    conn.send(pickle.dumps((player,BOARD_NUMBER_PIECES,BOARD_POSITION,BOARD_PIXEL_SIZE,EXTRA_PIECE_POSITION,int(BOARD_PIXEL_SIZE/BOARD_NUMBER_PIECES))))
    print("Connected to:",player)

    while True:
        try:
            player_data=pickle.loads(conn.recv(2048))
            
            if player_data == "Initial Board":
                print(player_data)
                conn.send(pickle.dumps(server_info.game_info[game_number]))
                
            
            elif player_data == "Waiting my turn":
                if server_info.game_info[game_number]:
                    conn.send(pickle.dumps(server_info.game_info[game_number]))
                else:
                    conn.send(pickle.dumps("Player Disconnected"))

            elif player_data == "Rotated Piece":
                if server_info.game_info[game_number]:
                    print(player_data)
                    server_info.game_info[game_number].extra_piece[1]+=1
                    if server_info.game_info[game_number].extra_piece[1]==4:
                        server_info.game_info[game_number].extra_piece[1]=0
                    conn.send(pickle.dumps(server_info.game_info[game_number]))
                
                else:
                    conn.send(pickle.dumps("Player Disconnected"))

            elif player_data[0]== "Inserting Piece":
                if server_info.game_info[game_number]: 
                    print(player_data[0])
                    server_info.game_info[game_number].extra_piece,server_info.game_info[game_number].move_player=extra_piece_insertion(server_info.game_info[game_number].move_player,server_info.game_info[game_number].extra_piece,server_info.game_info[game_number].board,player_data[1],player_data[2])
                    print(server_info.game_info[game_number])
                    conn.send(pickle.dumps(server_info.game_info[game_number]))
                else:
                    conn.send(pickle.dumps("Player Disconnected"))

            elif player_data[0] == "Moving Player":
                if server_info.game_info[game_number]:
                    print(player_data[0])
                    validity_board=validity_board_generator(server_info.game_info[game_number].board)
                    mouse_x_position=player_data[2]
                    mouse_y_position=player_data[1]
                    player_x_position=player_data[3]
                    player_y_position=player_data[4]

                    valid_move=move_validation(validity_board,None,mouse_y_position,mouse_x_position,player_x_position,player_y_position)
                    if valid_move and (server_info.game_info[game_number].board[mouse_y_position,mouse_x_position][2]==0 or server_info.game_info[game_number].board[mouse_y_position,mouse_x_position][2]==server_info.game_info[game_number].player):
                        server_info.game_info[game_number].board[player_y_position,player_x_position][2]=0
                        server_info.game_info[game_number].board[mouse_y_position,mouse_x_position][2]=server_info.game_info[game_number].player
    ################ Checking for treasure ######################
                        if server_info.game_info[game_number].board[mouse_y_position,mouse_x_position][3] != 0:
                            server_info.game_info[game_number].score[server_info.game_info[game_number].player-1]+=1
                            server_info.game_info[game_number].board[mouse_y_position,mouse_x_position][3]=0
                            while True:
                                yposition=random.randrange(0,BOARD_NUMBER_PIECES)
                                xposition=random.randrange(0,BOARD_NUMBER_PIECES)
                                if server_info.game_info[game_number].board[yposition,xposition][2] == 0:
                                    server_info.game_info[game_number].board[yposition,xposition][3]=1
                                    break
                        if server_info.game_info[game_number].player == TOTAL_PLAYERS:
                            server_info.game_info[game_number].player = 1
                        else:
                            server_info.game_info[game_number].player +=1
                        
                        server_info.game_info[game_number].move_player=False
                        conn.send(pickle.dumps(server_info.game_info[game_number]))
                        for i in range(TOTAL_PLAYERS):
                            print(f"Player {i+1}: {server_info.game_info[game_number].score[i]}")
    ################ Invalid player move ######################                
                    elif not valid_move or not (server_info.game_info[game_number].board[mouse_y_position,mouse_x_position][2]==0 or server_info.game_info[game_number].board[mouse_y_position,mouse_x_position][2]==server_info.game_info[game_number].player):
                        server_info.game_info[game_number].move_player=True
                        validity_board=validity_board_generator(server_info.game_info[game_number].board)
                        print("Invalid Player Move!")
                        conn.send(pickle.dumps(server_info.game_info[game_number]))
                        pass
                else:
                    conn.send(pickle.dumps("Player Disconnected"))

            elif player_data == "Disconnecting":
                conn.send(pickle.dumps("Disconnecting from Server"))
                server_info.connections[game_number]=[]
                server_info.game_info[game_number]=None
                conn.close()
                
            if not player_data:
                print( "Disconnected")
                break

        except:
            break
    print("Lost Connection")
    server_info.connections[game_number]=[]
    server_info.game_info[game_number]=None
    conn.close()

first_connect=True
while True:
    conn, addr=s.accept()

    if first_connect:
        server_info.connections=[[addr[1]]]
        m=movements()
        server_info.game_number=0
        server_info.player_number=server_info.connections[0].index(addr[1])+1
        m.board = initial_board_generator(BOARD_NUMBER_PIECES,NUMBER_OF_PIECES,NUMBER_OF_ROTATIONS,TOTAL_PLAYERS)
        server_info.game_info.append(m)
        
    else:
        for i in range(len(server_info.connections)):
            if len(server_info.connections[i])==0:

                server_info.connections[i]=[addr[1]]
                m=movements()
                server_info.game_number=i
                server_info.player_number=server_info.connections[i].index(addr[1])+1
                m.board = initial_board_generator(BOARD_NUMBER_PIECES,NUMBER_OF_PIECES,NUMBER_OF_ROTATIONS,TOTAL_PLAYERS)
                server_info.game_info[i]=m
                break

            elif len(server_info.connections[i])<TOTAL_PLAYERS:
                server_info.connections[i].append(addr[1])
                server_info.player_number=server_info.connections[i].index(addr[1])+1
                server_info.game_number=i
                break

            elif len(server_info.connections[i])==TOTAL_PLAYERS and i == len(server_info.connections)-1:
                server_info.connections.append([addr[1]])
                server_info.player_number=server_info.connections[i+1].index(addr[1])+1
                server_info.game_number=i+1

                m=movements()
                m.board = initial_board_generator(BOARD_NUMBER_PIECES,NUMBER_OF_PIECES,NUMBER_OF_ROTATIONS,TOTAL_PLAYERS)
                server_info.game_info.append(m)
                break

    start_new_thread(threaded_client,(conn,server_info.player_number,server_info.game_number))
    print(server_info.game_info)
    first_connect=False