import pygame
import random
import os
from pygame import mouse

WIDTH, HEIGHT = 1000, 980
BOARD_POSITION=[75,75]
BOARD_PIXEL_SIZE=280
BOARD_NUMBER_PIECES=7
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
YELLOW=(255,255,0)
BLUE=(0,0,255)
TURQUOISE=(0,255,255)
BLACK=(0,0,0)
FPS=25
TOTAL_PLAYERS=2
SQUARE_SIZE=int(BOARD_PIXEL_SIZE/BOARD_NUMBER_PIECES)
print(SQUARE_SIZE*3)
PLAYER_COLOURS=[RED,GREEN,BLUE,TURQUOISE]
NUMBER_OF_PIECES=[0,2,3]
NUMBER_OF_ROTATIONS=[0,1,2,3]
EXTRA_PIECE_X_POSITION=250
EXTRA_PIECE_Y_POSITION=800

board=[]
board_dict={}
validity_board=[]

WIN= pygame.display.set_mode((WIDTH,HEIGHT))

""" Each board piece has 4 parameters: [piece type, rotation of piece, player in piece, treasure in piece]
    Piece 0 is straight path, 1 is star, 2 is corner, 3 is T-junction; Rotation parameters coded into each piece generation code.
"""
def initial_board_generator(BOARD_NUMBER_PIECES,NUMBER_OF_PIECES,NUMBER_OF_ROTATIONS,TOTAL_PLAYERS):
    for i in range(BOARD_NUMBER_PIECES):
        boardx=[]
        for j in range (BOARD_NUMBER_PIECES):
            board_dict[(i,j)]=[random.choice(NUMBER_OF_PIECES),random.choice(NUMBER_OF_ROTATIONS),0,0]
            boardx.append([random.choice(NUMBER_OF_PIECES),random.choice(NUMBER_OF_ROTATIONS),0,0])
        board.append(boardx)
    if TOTAL_PLAYERS == 1:
        board[0][0][0]=2
        board[0][0][1]=0
        board[0][0][2]=1
    elif TOTAL_PLAYERS ==2:
        board[BOARD_NUMBER_PIECES-1][0][0]=board[0][0][0]=2
        board[0][0][1]=0
        board[BOARD_NUMBER_PIECES-1][0][1]=3
        board[0][0][2]=1
        board[BOARD_NUMBER_PIECES-1][0][2]=2
    elif TOTAL_PLAYERS ==3:
        board[0][BOARD_NUMBER_PIECES-1][0]=board[BOARD_NUMBER_PIECES-1][0][0]=board[0][0][0]=2
        board[0][0][1]=0
        board[BOARD_NUMBER_PIECES-1][0][1]=1
        board[0][BOARD_NUMBER_PIECES-1][1]=3
        board[0][0][2]=1
        board[BOARD_NUMBER_PIECES-1][0][2]=2
        board[0][BOARD_NUMBER_PIECES-1][2]=3
    elif TOTAL_PLAYERS == 4:
        board[BOARD_NUMBER_PIECES-1][BOARD_NUMBER_PIECES-1][0]=board[0][BOARD_NUMBER_PIECES-1][0]=board[BOARD_NUMBER_PIECES-1][0][0]=board[0][0][0]=2
        board[0][0][1]=0
        board[BOARD_NUMBER_PIECES-1][0][1]=1
        board[0][BOARD_NUMBER_PIECES-1][1]=3
        board[BOARD_NUMBER_PIECES-1][BOARD_NUMBER_PIECES-1][1]=2
        board[0][0][2]=1
        board[BOARD_NUMBER_PIECES-1][0][2]=2
        board[0][BOARD_NUMBER_PIECES-1][2]=3
        board[BOARD_NUMBER_PIECES-1][BOARD_NUMBER_PIECES-1][2]=4
    board[BOARD_NUMBER_PIECES//2][BOARD_NUMBER_PIECES//2][3]=1
    return board, board_dict

def validity_board_generator(board):
    validity_board=[]
    for i in board:
        boardx=[]
        for j in i:
            ###### Straight Piece ##############
            if j[0]==0 and (j[1]==0 or j[1]==2):
                boardx.append([0,1,0,1])
            elif j[0]==0 and (j[1]==1 or j[1]==3):
                boardx.append([1,0,1,0])
            ###### Star Piece ####################
            elif j[0]==1:
                boardx.append([1,1,1,1])
            ###### Corner Piece ####################
            elif j[0]==2 and j[1]==0:
                boardx.append([0,0,1,1])
            elif j[0]==2 and j[1]==1:
                boardx.append([0,1,1,0])
            elif j[0]==2 and j[1]==2:
                boardx.append([1,1,0,0])
            elif j[0]==2 and j[1]==3:
                boardx.append([1,0,0,1])
            ###### T-Junction Piece ################
            elif j[0]==3 and j[1]==0:
                boardx.append([1,0,1,1])
            elif j[0]==3 and j[1]==1:
                boardx.append([0,1,1,1])
            elif j[0]==3 and j[1]==2:
                boardx.append([1,1,1,0])
            elif j[0]==3 and j[1]==3:
                boardx.append([1,1,0,1])
        validity_board.append(boardx)
    return validity_board

"""movement -> board pieces are inserted with two coordinates (x,y) 
with x defining if piece is inserted vertically (0 bottom, 1 top) or horizontally (2 left, 3 right)
and y defining which collumn/row the piece is to be inserted into (index starting at 0)"""

def movingboard(piece=9,movement=None,board=None):
    horizontal_lenght=len(board[movement[1]]) #Number of collumns
    vertical_lenght=len(board) #Number of rows
    new_piece=piece
    #Vertical Movement
    if movement[0]==0: #Bottom to top   
        if board[0][movement[1]][2] != 0 or board[0][movement[1]][3] != 0:
            move_player=False
        else:
            new_piece=board[0][movement[1]]
            for i in range(0,vertical_lenght):
                if i == vertical_lenght-1:
                    board[i][movement[1]]=piece
                else:
                    board[i][movement[1]]=board[i+1][movement[1]]
            move_player=True         
    elif movement[0]==1: #Top to Bottom
        if board[vertical_lenght-1][movement[1]][2] != 0 or board[vertical_lenght-1][movement[1]][3]!= 0:
            move_player=False
        else:
            new_piece=board[vertical_lenght-1][movement[1]]
            for i in range(vertical_lenght-1,-1,-1):
                if i == 0:
                    board[i][movement[1]]=piece
                else:
                    board[i][movement[1]]=board[i-1][movement[1]]
            move_player=True
    #Horizontal Movement
    elif movement[0]==2: #Left to right
        if board[movement[1]][horizontal_lenght-1][2] == 0 and board[movement[1]][horizontal_lenght-1][3] == 0:
            new_piece=board[movement[1]][horizontal_lenght-1]
            board[movement[1]].insert(0,piece)
            board[movement[1]].pop(horizontal_lenght)
            move_player=True
        else:
            move_player=False
    elif movement[0]==3: #Right to left
        if board[movement[1]][0][2] == 0 and board[movement[1]][0][3] == 0:
            new_piece=board[movement[1]][0]
            board[movement[1]].insert(horizontal_lenght,piece)
            board[movement[1]].pop(0)
            move_player=True
        else:
            move_player=False
    if not move_player:
        print("Invalid, player or treasure would be removed from board")
    return new_piece,move_player

def draw_piece(piece,xposition,yposition,animation_frame,on_board=True):
    #pygame.draw.rect(Window to be drawn, colour, (left coord, top coord, width, height))
    loaded_image=False
    if not loaded_image:
        image=pygame.image.load(os.path.join("Assets",piece))
        loaded_image=True
    if on_board:
        board_position_x=xposition*SQUARE_SIZE*3+BOARD_POSITION[0]
        board_position_y=yposition*SQUARE_SIZE*3+BOARD_POSITION[1]+animation_frame
        # rotated_piece=pygame.transform.rotate(image,90*rotation)
        scaled_piece=pygame.transform.scale(image,(120,120))
        WIN.blit(scaled_piece,(board_position_x,board_position_y))
    else:
        board_position_x=xposition
        board_position_y=yposition
        # rotated_piece_extra=pygame.transform.rotate(image,90*rotation)
        scaled_piece_extra=pygame.transform.scale(image,(84,84))
        WIN.blit(scaled_piece_extra,(board_position_x,board_position_y))

def draw_players(xposition=None,yposition=None,player=None):
    board_position_x=xposition*SQUARE_SIZE*3+BOARD_POSITION[0]
    board_position_y=yposition*SQUARE_SIZE*3+BOARD_POSITION[1]
    pygame.draw.rect(WIN,PLAYER_COLOURS[player-1],(board_position_x+SQUARE_SIZE,     board_position_y+SQUARE_SIZE,     SQUARE_SIZE,SQUARE_SIZE))

def draw_treasure(xposition=None,yposition=None):
    board_position_x=xposition*SQUARE_SIZE*3+BOARD_POSITION[0]
    board_position_y=yposition*SQUARE_SIZE*3+BOARD_POSITION[1]
    pygame.draw.rect(WIN,YELLOW,(board_position_x+SQUARE_SIZE,     board_position_y+SQUARE_SIZE,     SQUARE_SIZE,SQUARE_SIZE))

def draw_board(board,tick):   
    yposition=0
    # if 0<=tick<=(1*FPS/12):
    #     animationframe1=0
    #     animationframe2=3
    # elif tick <=(2*FPS/12):
    #     animationframe1=1
    #     animationframe2=2
    
    # elif tick <=(3*FPS/12):
    #     animationframe1=2
    #     animationframe2=1
    
    # elif tick <=(4*FPS/12):
    #     animationframe1=3
    #     animationframe2=0
    
    # elif tick <=(5*FPS/12):
    #     animationframe1=2
    #     animationframe2=1
    
    # elif tick <=(6*FPS/12):
    #     animationframe1=1
    #     animationframe2=2
    
    # elif tick <=(7*FPS/12):
    #     animationframe1=0
    #     animationframe2=3
    
    # elif tick <=(8*FPS/12):
    #     animationframe1=1
    #     animationframe2=2
    
    # elif tick <=(9*FPS/12):
    #     animationframe1=2
    #     animationframe2=1
    
    # elif tick <=(10*FPS/12):
    #     animationframe1=3
    #     animationframe2=0
    
    # elif tick <=(11*FPS/12):
    #     animationframe1=2
    #     animationframe2=1
    
    # elif tick <=(12*FPS/12):
    #     animationframe1=1
    #     animationframe2=2
    # if 0<= tick <= FPS/2:
    #     animationframe1=int((tick*2/FPS)*5)

    # else:
    #     animationframe1=int((2-tick*2/FPS)*5)

    # if 0<tick<=FPS/4:
    #     animationframe2=int(((tick+FPS/4)/FPS)*10)
    # elif FPS/4<tick<=(3*FPS/4):
    #     animationframe2=int(((1-(tick+FPS/4)/FPS))*10)
    # else:
    #     animationframe2=int(((tick+FPS/4-FPS)/FPS)*10)
    count=0
    for i in board:
        xposition=0
        for j in i:
            if count==1:
                animationframe=0
                count=0
            else:
                animationframe=0
                count=1
            if j[0]==0:
                draw_piece(f"straight_{j[1]}.png",xposition,yposition,animationframe)
            elif j[0]==1:
                draw_piece(f"star.png",xposition,yposition,animationframe)
            elif j[0]==2:
                draw_piece(f"corner_{j[1]}.png",xposition,yposition,animationframe)
            elif j[0]==3:
                draw_piece(f"t_junction_{j[1]}.png",xposition,yposition,animationframe)
            if j[3]!=0:
                draw_treasure(xposition,yposition)
            if j[2]!=0:
                draw_players(xposition,yposition,j[2])
            xposition+=1
        yposition+=1
    return 0

def draw_extra_piece(piece=[]):
    # random.choice(NUMBER_OF_PIECES)
    if piece == []:
        piece.append(0)
        piece.append(0)
        piece.append(0)
        piece.append(0)
        if piece[0]==0:
                draw_piece(f"straight_{piece[1]}.png",EXTRA_PIECE_X_POSITION,EXTRA_PIECE_Y_POSITION,piece[1],on_board=False)
        elif piece[0]==1:
                draw_piece("star.png",EXTRA_PIECE_X_POSITION,EXTRA_PIECE_Y_POSITION,piece[1],on_board=False)
        elif piece[0]==2:
                draw_piece(f"corner_{piece[1]}.png",EXTRA_PIECE_X_POSITION,EXTRA_PIECE_Y_POSITION,piece[1],on_board=False)
        elif piece[0]==3:
                draw_piece(f"t_junction_{piece[1]}.png",EXTRA_PIECE_X_POSITION,EXTRA_PIECE_Y_POSITION,piece[1],on_board=False)  
        return piece
    elif piece != []:
        if piece[0]==0:
                draw_piece(f"straight_{piece[1]}.png",EXTRA_PIECE_X_POSITION,EXTRA_PIECE_Y_POSITION,piece[1],on_board=False)
        elif piece[0]==1:
                draw_piece(f"star.png",EXTRA_PIECE_X_POSITION,EXTRA_PIECE_Y_POSITION,piece[1],on_board=False)
        elif piece[0]==2:
                draw_piece(f"corner_{piece[1]}.png",EXTRA_PIECE_X_POSITION,EXTRA_PIECE_Y_POSITION,piece[1],on_board=False)
        elif piece[0]==3:
                draw_piece(f"t_junction_{piece[1]}.png",EXTRA_PIECE_X_POSITION,EXTRA_PIECE_Y_POSITION,piece[1],on_board=False)
        return piece

def draw_win():
    WIN.fill(BLACK)

def extra_piece_rotation(event,extra_piece):
    keys=pygame.key.get_pressed()
    if event.type == pygame.KEYDOWN:
        if keys[pygame.K_r]:
            print("PRESSED R")
            extra_piece[1]+=1
            if extra_piece[1]==4:
                extra_piece[1]=0
            draw_extra_piece(extra_piece)

def extra_piece_insertion(move_player,event,extra_piece,validity_board):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[0]:
            mouse_x_position=int((pygame.mouse.get_pos()[0]-BOARD_POSITION[0])//(SQUARE_SIZE*3))
            mouse_y_position=int((pygame.mouse.get_pos()[1]-BOARD_POSITION[0])//(SQUARE_SIZE*3))
            if mouse_y_position==-1 and mouse_x_position<=BOARD_NUMBER_PIECES-1 and mouse_x_position>=0:
                new_piece,move_player=movingboard(extra_piece,(1,mouse_x_position),board) 
            elif mouse_y_position==BOARD_NUMBER_PIECES and mouse_x_position<=BOARD_NUMBER_PIECES-1 and mouse_x_position>=0:
                new_piece,move_player=movingboard(extra_piece,(0,mouse_x_position),board)
            elif mouse_x_position==-1 and mouse_y_position<=BOARD_NUMBER_PIECES-1 and mouse_y_position>=0:
                new_piece,move_player=movingboard(extra_piece,(2,mouse_y_position),board)
            elif mouse_x_position==BOARD_NUMBER_PIECES and mouse_y_position<=BOARD_NUMBER_PIECES-1 and mouse_y_position>=0:
                new_piece,move_player=movingboard(extra_piece,(3,mouse_y_position),board)
            else:
                print("Invalid, not clicking on appropriate places")
                return extra_piece, move_player,validity_board
            extra_piece=draw_extra_piece(new_piece)
            validity_board=validity_board_generator(board)
            return extra_piece, move_player,validity_board
    return extra_piece, move_player,validity_board

def move_validation(checking_board,input_direction,mouse_y_position,mouse_x_position,player_x_position,player_y_position):      
    valid_move=False
    input_direction_original=input_direction
    if mouse_y_position==player_y_position and mouse_x_position==player_x_position:
        return True
    if input_direction=="Right":
        pass
    else:
        if checking_board[player_y_position][player_x_position][0]==1 and player_x_position!=0:
            if checking_board[player_y_position][player_x_position-1][2]==1:
                checking_board[player_y_position][player_x_position][0]=0
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
        if checking_board[player_y_position][player_x_position][1]==1 and player_y_position != 0:
            if checking_board[player_y_position-1][player_x_position][3]==1:
                checking_board[player_y_position][player_x_position][1]=0
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
        if checking_board[player_y_position][player_x_position][2]==1 and player_x_position!=len(checking_board)-1:
            if checking_board[player_y_position][player_x_position+1][0]==1:
                checking_board[player_y_position][player_x_position][2]=0
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
        if checking_board[player_y_position][player_x_position][3]==1 and player_y_position != len(checking_board)-1:
            if checking_board[player_y_position+1][player_x_position][1]==1:
                checking_board[player_y_position][player_x_position][3]=0
                player_y_position+=1
                input_direction="Down"
                valid_move=move_validation(checking_board,input_direction,mouse_y_position,mouse_x_position,player_x_position,player_y_position)
                if valid_move:
                    return valid_move
                player_y_position-=1
                input_direction=input_direction_original
    return valid_move

def main():
    clock=pygame.time.Clock()
    board, board_dict = initial_board_generator(BOARD_NUMBER_PIECES,NUMBER_OF_PIECES,NUMBER_OF_ROTATIONS,TOTAL_PLAYERS)
    extra_piece=[]
    validity_board=[]
    run=True
    draw_win()
    move_player=False
    player = 1
    score=[0 for i in range(TOTAL_PLAYERS)]
    first_board=True
    tick=1
    while run:
        clock.tick(FPS)
        if first_board:
            draw_board(board,tick)
            first_board=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
####################### Rotating and inserting extra piece in board #####################################################
            if not move_player:
                extra_piece_rotation(event,extra_piece)
                extra_piece, move_player,validity_board=extra_piece_insertion(move_player,event,extra_piece,validity_board)
                if move_player:
                    print("Valid Piece Movement")
                    
####################### Moving player piece #####################################################
            elif move_player:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mouse_x_position=int((pygame.mouse.get_pos()[0]-BOARD_POSITION[0])//(SQUARE_SIZE*3))
                        mouse_y_position=int((pygame.mouse.get_pos()[1]-BOARD_POSITION[0])//(SQUARE_SIZE*3))
                        #Player Position#
                        for i in range(len(board)):
                            for j in range(len(board[0])):
                                if board[i][j][2]==player:
                                    player_y_position,player_x_position = i,j 
                                    break
                        valid_move=move_validation(validity_board,None,mouse_y_position,mouse_x_position,player_x_position,player_y_position)                      
                        if valid_move and (board[mouse_y_position][mouse_x_position][2]==0 or board[mouse_y_position][mouse_x_position][2]==player):
                            print("Valid Player Move")
                            board[player_y_position][player_x_position][2]=0
                            board[mouse_y_position][mouse_x_position][2]=player
####################### Checking if treasure on piece #####################################################
                            if board[mouse_y_position][mouse_x_position][3] != 0:
                                score[player-1]+=1
                                board[mouse_y_position][mouse_x_position][3]=0
                                while True:
                                    yposition=random.randrange(0,BOARD_NUMBER_PIECES)
                                    xposition=random.randrange(0,BOARD_NUMBER_PIECES)
                                    if board[yposition][xposition][2] == 0:
                                        board[yposition][xposition][3]=1
                                        break
####################### Printing score #####################################################                                
                                print("Score:")
                                if TOTAL_PLAYERS == 1:
                                    print(f"P1 - {score[0]}")
                                elif TOTAL_PLAYERS ==2:
                                    print(f"P1 - {score[0]}\nP2 - {score[1]}")
                                elif TOTAL_PLAYERS ==3:
                                    print(f"P1 - {score[0]}\nP2 - {score[1]}\nP3 - {score[2]}")
                                elif TOTAL_PLAYERS == 4:
                                    print(f"P1 - {score[0]}\nP2 - {score[1]}\nP3 - {score[2]}\nP4 - {score[3]}")
####################### Changing turn between players #####################################################                                
                            move_player=False
                            if player == TOTAL_PLAYERS:
                                player = 1
                            else:
                                player +=1
                        else:
                            move_player=True
                            validity_board=validity_board_generator(board)
                            print("Invalid Player Move!")
                            pass
        if extra_piece == []:
            extra_piece=draw_extra_piece()
        draw_board(board,tick)
        pygame.display.update()
        if tick == FPS:
            tick = 1
        else:
            tick+=1
    pygame.quit()
if __name__=="__main__":
    main()