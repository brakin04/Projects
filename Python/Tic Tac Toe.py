import random 
# Tic Tac Toe
def print_board(board):
    count = 0
    for row in board:
        print(" | ".join(row))
        if count != 2:
            print("-"*9)
        else: 
            print("\n")
        count+=1

def print_num_board():
    print("0 | 1 | 2\n---------\n3 | 4 | 5\n---------\n6 | 7 | 8\n")

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                return False
    return True
def tic_tac_toe():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    players = ['X', 'O']
    pT = 0

    pinput = input("Choose X or O: ")
    while True:
        if pinput.upper() == 'X':
            pT = 0;
            break;
        elif pinput.upper() == "O":
            pT = 1;
            break;
        else: 
            pinput = input("Try again: X or O? ")
    while True:
        if pT == 0: 
            pplay = playerGo(board, 'X');
            print("You played: ", pplay)
            board[pplay // 3][pplay % 3] = 'X';
            if check_winner(board, 'X'):
                print("X's win!");
                print_board(board);
                break;
            elif is_full(board):
                print("Tie, nobody wins");
                print_board(board);
                break;
            bplay = botGo(board, "O");
            print("Bot played: ", bplay)
            board[bplay // 3][bplay % 3] = 'O';
            if check_winner(board, 'O'):
                print("O's win!")
                print_board(board);
                break;
            if is_full(board):
                print("Tie, nobody wins");
                print_board(board);
                break;
        elif pT == 1: 
            bplay = botGo(board, "X");
            print("Bot played: ", bplay)
            board[bplay // 3][bplay % 3] = 'X';
            if check_winner(board, 'X'):
                print("X's win!");
                print_board(board);
                break;
            if is_full(board):
                print("Tie, nobody wins");
                print_board(board);
                break;
            pplay = playerGo(board, 'O');
            print("You played: ", pplay)
            board[pplay // 3][pplay % 3] = 'O';
            if check_winner(board, 'O'):
                print("O's win!");
                print_board(board);
                break;
            elif is_full(board):
                print("Tie, nobody wins");
                print_board(board);
                break;
    again = input("Play again? Y/n: ")
    another = False
    while True:
        if again == 'y' or again == 'Y':
            another = True
            break;
        elif again == 'n' or again == 'N':
            another = False
            break;
        else:
            again = input("Enter Y or n: ");
    if another:
        tic_tac_toe();
    

#Python matrix[1][2] gives 3rd element in second row  
# it shows ___[row][col]
def open_spots(board):
    open_spot = []
    for i in range(3):
        for j in range(3):
            if board[j][i] == " ":
                open_spot.append(j*3 + i)
                #print(j, " ", i) 
            #else:
                #print("Used: ", j, " ", i)
    return open_spot

def playerGo(board, team):
    open_spot = open_spots(board)
    print_num_board();
    print_board(board);
    while True:
        try:
            user_input = input("Choose a play 0-8: ")
            play = int(user_input)
        except ValueError:
            play = -1
            print("Not a number, try again")
        if play < 0 or play > 8:
            print("Try again");
        elif play not in open_spot: 
            print("This spot is not open");
        else:
            break;
    return play


def botGo(board, team):
    open_spot = open_spots(board);
    opp = "O"
    if team == "O":
        opp = "X"
    #Win 
    #Rows 
    if board[0][0] == team and board[0][1] == team and 2 in open_spot:
        return 2
    elif board[0][0] == team and board[0][2] == team and 1 in open_spot:
        return 1
    elif board[0][1] == team and board[0][2] == team and 0 in open_spot:
        return 0
    elif board[1][0] == team and board[1][1] == team and 5 in open_spot:
        return 5
    elif board[1][0] == team and board[1][2] == team and 4 in open_spot:
        return 4
    elif board[1][2] == team and board[1][1] == team and 3 in open_spot:
        return 3
    elif board[2][0] == team and board[2][1] == team and 8 in open_spot:
        return 8
    elif board[2][0] == team and board[2][2] == team and 7 in open_spot:
        return 7
    elif board[2][2] == team and board[2][1] == team and 6 in open_spot:
        return 6
    #Columns
    elif board[0][0] == team and board[1][0] == team and 6 in open_spot:
        return 6
    elif board[0][0] == team and board[2][0] == team and 3 in open_spot:
        return 3
    elif board[2][0] == team and board[1][0] == team and 0 in open_spot:
        return 0
    elif board[0][1] == team and board[1][1] == team and 7 in open_spot:
        return 7
    elif board[0][1] == team and board[2][1] == team and 4 in open_spot:
        return 4
    elif board[2][1] == team and board[1][1] == team and 1 in open_spot:
        return 1
    elif board[0][2] == team and board[1][2] == team and 8 in open_spot:
        return 8
    elif board[0][2] == team and board[2][2] == team and 5 in open_spot:
        return 5
    elif board[2][2] == team and board[1][2] == team and 2 in open_spot:
        return 2
    #diagonal
    elif board[0][0] == team and board[1][1] == team and 8 in open_spot:
        return 8
    elif board[0][0] == team and board[2][2] == team and 4 in open_spot:
        return 4
    elif board[1][1] == team and board[2][2] == team and 0 in open_spot:
        return 0
    elif board[2][0] == team and board[0][2] == team and 4 in open_spot:
        return 4
    elif board[2][0] == team and board[1][1] == team and 2 in open_spot:
        return 2
    elif board[1][1] == team and board[0][2] == team and 6 in open_spot:
        return 6

    #block
    #Columns 
    elif board[0][0] == opp and board[0][1] == opp and 2 in open_spot:
        return 2
    elif board[0][0] == opp and board[0][2] == opp and 1 in open_spot:
        return 1
    elif board[0][1] == opp and board[0][2] == opp and 0 in open_spot:
        return 0
    elif board[1][0] == opp and board[1][1] == opp and 5 in open_spot:
        return 5
    elif board[1][0] == opp and board[1][2] == opp and 4 in open_spot:
        return 4
    elif board[1][2] == opp and board[1][1] == opp and 3 in open_spot:
        return 3
    elif board[2][0] == opp and board[2][1] == opp and 8 in open_spot:
        return 8
    elif board[2][0] == opp and board[2][2] == opp and 7 in open_spot:
        return 7
    elif board[2][2] == opp and board[2][1] == opp and 6 in open_spot:
        return 6
    #rows
    elif board[0][0] == opp and board[1][0] == opp and 6 in open_spot:
        return 6
    elif board[0][0] == opp and board[2][0] == opp and 3 in open_spot:
        return 3
    elif board[2][0] == opp and board[1][0] == opp and 0 in open_spot:
        return 0
    elif board[0][1] == opp and board[1][1] == opp and 7 in open_spot:
        return 7
    elif board[0][1] == opp and board[2][1] == opp and 4 in open_spot:
        return 4
    elif board[2][1] == opp and board[1][1] == opp and 1 in open_spot:
        return 1
    elif board[0][2] == opp and board[1][2] == opp and 8 in open_spot:
        return 8
    elif board[0][2] == opp and board[2][2] == opp and 5 in open_spot:
        return 5
    elif board[2][2] == opp and board[1][2] == opp and 2 in open_spot:
        return 2
    #diagonal
    elif board[0][0] == opp and board[1][1] == opp and 8 in open_spot:
        return 8
    elif board[0][0] == opp and board[2][2] == opp and 4 in open_spot:
        return 4
    elif board[1][1] == opp and board[2][2] == opp and 0 in open_spot:
        return 0
    elif board[2][0] == opp and board[0][2] == opp and 4 in open_spot:
        return 4
    elif board[2][0] == opp and board[1][1] == opp and 2 in open_spot:
        return 2
    elif board[1][1] == opp and board[0][2] == opp and 6 in open_spot:
        return 6

    #play
    elif board[1][1] == " ":
        return 4
    else:
        while True:
            rand = random.randint(0,8)
            if rand in open_spot:
                return rand

    #choose random integer rand = randint(0,8) and check if board[rand % 3][rand / 3] == ' '
        

    
if __name__ == "__main__":
    tic_tac_toe();