# import matplotlib.patches as patches
# import matplotlib.pyplot as plt

#Move generator
def actions(board_, player):
        """Return a list of the allowable moves at this point."""
        validMoves = []
        board = copy_board(board_)
        for row in range(8):
            for col in range(8):
                if isValidMove(board,player,row,col):
                    validMoves.append([row,col])
        return validMoves
#Makes sure query is in bounds of board
def isOnBoard(row,col):
    return (row <= 7 and row >= 0 and col <= 7 and col >= 0)
#Conveniently return opponent player
def opponent(player):
    if(player == 'W'):
        return 'B'
    else:
        return 'W'

#Makes copy of entire board state. Used alot to prevent mutable confusions
def copy_board(board):
    board_copy = []
    for row in range(8):
        board_copy.append([' ']*8)
    for row in range(8):
        for col in range(8):
            board_copy[row][col] = board[row][col]
    return board_copy
def new_board():
    new_board = []
    for row in range(8):
        new_board.append([' ']*8)
    return new_board
def make_move(board_,player,m):
    board = copy_board(board_)
    to_flip = isValidMove(board,player,m[0],m[1])
    if to_flip:
        board[m[0]][m[1]] = player
        for row,col in to_flip:
            board[row][col] = player
    return board

#Returns difference of # tiles between player and opponent
def score(board, player):
    player_score, opponent_score = 0, 0
    opponent_p = opponent(player)
    for row in range(8):
        for col in range(8):
            if(board[row][col] != ' '):
                if board[row][col] == player:
                    player_score += 1
                elif board[row][col] == opponent_p:
                    opponent_score += 1
    return player_score - opponent_score

#Is it a corner? corners are good...
def isCorner(row,col):
    return((row == 0 and col == 0) or (row == 0 and col == 7) or (row == 7 and col == 7) or (row == 7  and col == 0))

#Returns difference in score, like score, but heavily weights corners.
def score_corners(board,player):
    player_score, opponent_score = 0, 0
    opponent_p = opponent(player)
    for row in range(8):
        for col in range(8):
            if(board[row][col] != ' '):
                if board[row][col] == player:
                    if isCorner(row,col):
                        player_score += 15
                    else:
                        player_score += 1
                elif board[row][col] == opponent_p:
                    if isCorner(row,col):
                        opponent_score += 15
                    else:
                        opponent_score += 1
    return player_score - opponent_score

#Alpha beta algorithm with depth cutoff. Specify evaluation function. Depths > 5 take a very long time
#Credit to D H Connelly for inspiring this alpha/beta implementation http://dhconnelly.com/paip-python/docs/paip/othello.html
def alpha_beta(board,player,alpha,beta,depth,evaluate):
    if depth == 0:
        return evaluate(board,player), None
    def value(board,alpha,beta):
        return - alpha_beta(board,opponent(player),-beta,-alpha,depth-1,evaluate)[0]
    moves = actions(board,player)
    if not moves:
        if not actions(board ,opponent(player)):
            return final_val(board,player), None
        return value(board,alpha,beta), None
    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            break
        val = value(make_move(board, player,move), alpha,beta)
        if val > alpha:
            alpha = val
            best_move = move
    return alpha, best_move

#Initializes the board config to start the game
def start_config(board):
    board[3][3], board[4][3] = 'B','W'
    board[3][4], board[4][4] = 'W','B'
def n_pieces(board):
    n = 0
    for i in range(8):
        for j in range(8):
            if(board[i][j] != ' '):
                n += 1
    return n

#check if move is valid and which tiles would be flipped as a result
#This is done by looking along the 8 principle directions
def isValidMove(board_,player,row_s,col_s):
    board = copy_board(board_)
    if board[row_s][col_s] != ' ' or not isOnBoard(row_s,col_s):
        return False
    board[row_s][col_s] = player
    other_player = opponent(player)
    flip_tiles = []
    for row_d,col_d in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
        row,col = row_s,col_s
        row += row_d
        col += col_d
        if isOnBoard(row,col) and board[row][col] == other_player:
            row += row_d
            col += col_d
            if not isOnBoard(row,col):
                continue
            while board[row][col] == other_player:
                row += row_d
                col += col_d
                if not isOnBoard(row,col):
                    break
            if not isOnBoard(row,col):
                continue
            if board[row][col] == player:
                while True:
                    row -= row_d
                    col -= col_d
                    if row == row_s and col == col_s:
                        break
                    flip_tiles.append([row,col])
    board[row_s][col_s] = ' '
    if len(flip_tiles) == 0:
        return False
    return flip_tiles

#Prints out nice terminal board
def disp_board(board):
    print('-----------------')
    for i in range(8):
        line_str = '|'
        for j in range(8):
            line_str += board[i][j] +'|'
        print(line_str )
        print('-----------------')
# def disp_graphic_board(board,ax):
#     ax.set_facecolor('g')
#     for j in range(8):
#         for i in range(8):
#             if board[i][j] != ' ':
#                 if(board[i][j] == 'W' ):
#                     color = 'white'
#                 elif(board[i][j] == 'B' ):
#                     color = 'black'
#                 ax.add_patch(patches.Circle([i, j],.2,facecolor = color))

#     plt.axis('equal')

#This used to heavily weight the terminal state of the game. If a move results in loss,
#it should be heavily penalized. Same for winning.
def final_val(board_, player):
    diff = score(copy_board(board_),player)
    if diff < 0:
        return -1000
    elif diff > 0:
        return 1000
    return diff

def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#CONFIG###########
board = new_board()
start_config(board)
cpu_depth_cutoff = 3
cpu_corner_greedy = True
##################

print('Welcome to Othello')
print('Your cpu opponent is set at skill level: {}'.format(cpu_depth_cutoff))
if cpu_corner_greedy:
    print('Your cpu opponent is corner greedy')
print('You have the first move!')    
disp_board(board)
player = 'B'
opp = opponent(player)
over = False
i = 1
while not over:
    print("Turn: {}".format(i))
    i += 1
    no_move_p = False
    no_move_op = False
    board_copy = copy_board(board)
    #alpha, move = alpha_beta(board_copy,player,-1000,1000,3,score_corners)
    moves = actions(board,player)
    if moves:
        print("Your available moves [row,col]: {}".format(moves))
        no_good_input = True
        while(no_good_input):
            row = input('enter move row: ')
            col = input('enter move col: ')
            if(representsInt(row) and representsInt(col)):
                row = int(row)
                col = int(col)
                if(row >= 0 and row < 8 and col >= 0 and col < 8):
                    no_good_input = False
            if(no_good_input):
                print("Please enter only valid integers 0 - 7")
        board = make_move(board,player,[row,col])
    else:
        moves= actions(board,player)
        print("NO MOVES {}".format(player))
        no_move_p = True

    alpha = None
    move = None
    print("You made a move")
    disp_board(board)
    board_copy = copy_board(board)
    print('Thinking...')
    if(cpu_corner_greedy):
        alpha, move = alpha_beta(board_copy,opp,-1000,1000,cpu_depth_cutoff,score_corners)
    else:
        alpha, move = alpha_beta(board_copy,opp,-1000,1000,cpu_depth_cutoff,score)
    if move:
        board = make_move(board,opp,move)
        print("Your opponent made a move, row: {}, col: {}".format(move[0],move[1]))
    else:
        moves = actions(board,opp)
        print("NO MOVES {}".format(opp))
        no_move_op = True
    
    move = None
    alpha = None
    disp_board(board)
    if(no_move_p and no_move_op):
        over = True
final_score_B = score(board,'B')
final_score_W = score(board,'W')
if(final_score_B > final_score_W):
    print('You win!')
elif(final_score_W > final_score_B):
    print('You lose :(')
else:
    print('Tie?')
print(final_score_B,final_score_W)

