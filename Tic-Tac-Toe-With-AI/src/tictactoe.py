import math
import tkinter as tk

board = [[' ' for _ in range (3)] for _ in range (3)] # 3x3 board

def print_board():
    for row in board:
        print('|'.join(row))
        print('-'*5)

def is_winner(board, player):
    for row in board:
        if all([cell == player for cell in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

def is_board_full(board):
    return all([cell != ' ' for row in board for cell in row])

def minimax(board, depth, is_maximizing):
    if is_winner(board, 'X'):
        return -1
    if is_winner(board, 'O'):
        return 1
    if is_board_full(board):
        return 0
    
    if is_maximizing :
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth+1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth+1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def on_click(row, col):
    if board[row][col] == ' ':
        board[row][col] = 'X'
        buttons[row][col].config(text='X')
        if is_winner(board, player='X'):
            result_label.config(text='You Win!')
            disable_buttons()
            return
        if is_board_full(board):
            result_label.config(text="It's a tie!")
            return
        
        move = best_move(board)
        if move:
            board[move[0]][move[1]] = 'O'
            buttons[move[0]][move[1]].config(text='O')
            if is_winner(board, player='O'):
                result_label.config(text="AI wins!")
                disable_buttons()
                return 
            if is_board_full(board):
                result_label.config(text="It's a tie!")
                return
            
def disable_buttons():
    for row in buttons:
        for button in row:
            button.config(state=tk.DISABLED)

def reset_game():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=' ', state=tk.NORMAL)
    result_label.config(text='')

root = tk.Tk()
root.title('Tic Tac Toe')

buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text=' ', font=('normal', 40), width=5, height=2,
                                  command=lambda i=i, j=j: on_click(i, j))
        buttons[i][j].grid(row=i, column=j)

result_label = tk.Label(root, text="", font=('normal', 20))
result_label.grid(row=3, column=0, columnspan=3)
restart_button = tk.Button(root, text='Restart', font=('normal', 20), command=reset_game)
restart_button.grid(row=4, column=0, columnspan=3)



root.mainloop()