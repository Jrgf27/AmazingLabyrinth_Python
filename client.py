from network import Network
from game_info import movements
import pygame
import os
import time

WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
YELLOW=(255,255,0)
BLUE=(0,0,255)
TURQUOISE=(0,255,255)
BLACK=(0,0,0)
WIDTH, HEIGHT = 900,900
FPS=60
PLAYER_COLOURS=["player1.png","player2.png","player3.png","player4.png"]

pygame.init()
WIN= pygame.display.set_mode((WIDTH,HEIGHT))

def draw_text(text,color,pos,font):
    message=font.render(text, True , color)
    WIN.blit(message,pos)

def draw_piece(piece,xposition,yposition,rotation,info,on_board=True):
    #pygame.draw.rect(Window to be drawn, colour, (left coord, top coord, width, height))
    loaded_image=False
    if not loaded_image:
        image=pygame.image.load(os.path.join("Assets",piece))
        loaded_image=True
    if on_board:
        board_position_x=int(xposition*info.square_size*3+info.board_pos[0])
        board_position_y=int(yposition*info.square_size*3+info.board_pos[1])
        rotated_piece=pygame.transform.rotate(image,90*rotation)
        scaled_piece=pygame.transform.scale(rotated_piece,(info.square_size*3,info.square_size*3))
        WIN.blit(scaled_piece,(board_position_x,board_position_y))
    else:
        board_position_x=int(xposition)
        board_position_y=int(yposition)
        rotated_piece_extra=pygame.transform.rotate(image,90*rotation)
        scaled_piece_extra=pygame.transform.scale(rotated_piece_extra,(75,75))
        WIN.blit(scaled_piece_extra,(board_position_x,board_position_y))

def draw_players(xposition,yposition,player,info):

    image=pygame.image.load(os.path.join("Assets",PLAYER_COLOURS[player-1]))
    board_position_x=int(xposition*info.square_size*3+info.board_pos[0]+info.square_size)
    board_position_y=int(yposition*info.square_size*3+info.board_pos[1]+info.square_size)
    scaled_piece=pygame.transform.scale(image,(info.square_size,info.square_size))
    WIN.blit(scaled_piece,(board_position_x,board_position_y))
    
def draw_treasure(xposition,yposition,info):

    image=pygame.image.load(os.path.join("Assets","treasure.png"))
    board_position_x=int(xposition*info.square_size*3+info.board_pos[0]+info.square_size)
    board_position_y=int(yposition*info.square_size*3+info.board_pos[1]+info.square_size)
    scaled_piece=pygame.transform.scale(image,(info.square_size,info.square_size))
    WIN.blit(scaled_piece,(board_position_x,board_position_y))

def draw_board(board,info):   
    yposition=0
    for i in board:
        xposition=0
        for j in i:
            if j[0]==0:
                draw_piece("straight.png",xposition,yposition,j[1],info)
            elif j[0]==1:
                draw_piece("star.png",xposition,yposition,j[1],info)
            elif j[0]==2:
                draw_piece("corner.png",xposition,yposition,j[1],info)
            elif j[0]==3:
                draw_piece("t_junction.png",xposition,yposition,j[1],info)
            if j[3]!=0:
                draw_treasure(xposition,yposition,info)
            if j[2]!=0:
                draw_players(xposition,yposition,j[2],info)
            xposition+=1
        yposition+=1
    return 0

def draw_extra_piece(piece,info):
    if piece[0]==0:
            draw_piece("straight.png",info.extra_piece_pos[0],info.extra_piece_pos[1],piece[1],info,on_board=False)
    elif piece[0]==1:
            draw_piece("star.png",info.extra_piece_pos[0],info.extra_piece_pos[1],piece[1],info,on_board=False)
    elif piece[0]==2:
            draw_piece("corner.png",info.extra_piece_pos[0],info.extra_piece_pos[1],piece[1],info,on_board=False)
    elif piece[0]==3:
            draw_piece("t_junction.png",info.extra_piece_pos[0],info.extra_piece_pos[1],piece[1],info,on_board=False)
    return piece

def game_window(m,info,total_players):
    WIN.fill(WHITE)
    draw_board(m.board,info)
    draw_extra_piece(m.extra_piece,info)
    exit_game_session=pygame.draw.rect(WIN,(0,0,0),[800,800,100,100])
    font = pygame.font.SysFont(None, 25)
    
    for i in range(total_players):
        posx=50+100*i
        posy=50
        draw_text(f"Player {i+1}: {m.score[i]}",BLACK,(posx,posy),font)

def draw_initial_menu():
    WIN.fill(WHITE)
    start_1v1_game=pygame.draw.rect(WIN,(0,0,0),[100,100,100,100])

def main():
    clock=pygame.time.Clock()
    run=True
    game_state="Initial Menu"
    initial_info=False
    tick=1
    while run:
        clock.tick(FPS)
        pygame.display.update()
        
        if game_state=="Initial Menu":
            draw_initial_menu()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mouse_x_position=pygame.mouse.get_pos()[0]
                        mouse_y_position=pygame.mouse.get_pos()[1]
                        if 100 <= mouse_x_position <= 200 and 100 <= mouse_y_position <= 200:
                            game_state="Game Ongoing"
                            TOTAL_PLAYERS=2
                            print("Button Clicked")
        
        if game_state == "Game Ongoing":
            if not initial_info:
                info=Network(TOTAL_PLAYERS)
                playerID=info.player
                m=info.send("Initial Board")
                initial_info=True
                game_window(m,info,TOTAL_PLAYERS)
                start=time.time()

            if m.player != playerID:
                time_to_send=time.time()-start
                print(time_to_send)
                if time_to_send >= 2:
                    n=info.send("Waiting my turn")
                    if n == "Player Disconnected":
                        game_state="Initial Menu"
                        initial_info=False
                        print(info.send("Disconnecting"))
                    elif n == "No Inputs":
                        start=time.time()
                        pass
                    else:
                        m=n
                        game_window(m,info,TOTAL_PLAYERS)
                        start=time.time()
                        
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mouse_x_position=pygame.mouse.get_pos()[0]
                        mouse_y_position=pygame.mouse.get_pos()[1]
                        if 800 <= mouse_x_position <= 900 and 800 <= mouse_y_position <= 900:
                            game_state="Initial Menu"
                            initial_info=False
                            print(info.send("Disconnecting"))
                            break
                
                if m.player==playerID:
                    if not m.move_player:
    ############################### Rotation Input
                        keys=pygame.key.get_pressed()
                        if event.type == pygame.KEYDOWN:
                            if keys[pygame.K_r]:
                                print("PRESSED R")
                                m=info.send("Rotated Piece")
                                if m == "Player Disconnected":
                                    game_state="Initial Menu"
                                    initial_info=False
                                    print(info.send("Disconnecting"))
                                    break
                                else:
                                    draw_extra_piece(m.extra_piece,info)     
                                    
    ############################### Piece Movement
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                mouse_x_position=int((pygame.mouse.get_pos()[0]-info.board_pos[0])//(info.square_size*3))
                                mouse_y_position=int((pygame.mouse.get_pos()[1]-info.board_pos[0])//(info.square_size*3))
                                m=info.send(("Inserting Piece", mouse_x_position, mouse_y_position))
                                if m == "Player Disconnected":
                                    game_state="Initial Menu"
                                    initial_info=False
                                    print(info.send("Disconnecting"))
                                    break

                        if m.move_player:
                            print("Valid Piece Movement")
    ############################### Piece Movement            
                    if m.move_player:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed()[0]:
                                mouse_x_position=int((pygame.mouse.get_pos()[0]-info.board_pos[0])//(info.square_size*3))
                                mouse_y_position=int((pygame.mouse.get_pos()[1]-info.board_pos[0])//(info.square_size*3))
        ####################### Player Position#
                                for i in range(len(m.board)):
                                    for j in range(len(m.board[0])):
                                        if m.board[i][j][2]==m.player:
                                            player_y_position,player_x_position = i,j 
                                            break
    ########################### Move Validation                            
                                m=info.send(("Moving Player", mouse_y_position,mouse_x_position,player_x_position,player_y_position))     
                                if m == "Player Disconnected":
                                    game_state="Initial Menu"
                                    initial_info=False
                                    print(info.send("Disconnecting"))
                                    break
                                game_window(m,info,TOTAL_PLAYERS)
        if tick==FPS:
            tick = 1
        else:
            tick+=1
    pygame.quit()

if __name__=="__main__":
    main()