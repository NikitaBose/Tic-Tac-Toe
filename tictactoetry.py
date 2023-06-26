import tkinter as tk
from tkinter import messagebox

import pygame
from pygame import mixer 

pygame.mixer.init()
computer_move_sound = pygame.mixer.Sound(r'C:\Users\Nikita\Desktop\tictactoe\correct.wav')

# Create the main window
root = tk.Tk()
root.title("Tic Tac Toe")

# Initialize game variables
player = "X"
computer = "O"
board = [" " for _ in range(9)]


def check_win():
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != " ":
            return True

    # Check columns
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != " ":
            return True

    # Check diagonals
    if board[0] == board[4] == board[8] != " " or board[2] == board[4] == board[6] != " ":
        return True

    return False


def check_draw():
    return " " not in board


def restart_game():
    global board
    board = [" " for _ in range(9)]
    reset_board()


def make_move(index):
    # Check if the selected position is empty
    if board[index] == " ":
        board[index] = player
        buttons[index].config(text=player, state=tk.DISABLED)

        if check_win():
            messagebox.showinfo("Game Over", f"Player {player} wins!")
            restart_game()
        elif check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            restart_game()
        else:
            computer_move()


def computer_move():
    best_score = float('-inf')
    best_move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = computer
            score = minimax(board, 0, False)
            board[i] = " "

            if score > best_score:
                best_score = score
                best_move = i   
            computer_move_sound.play()         

    board[best_move] = computer
    buttons[best_move].config(text=computer, state=tk.DISABLED)

    if check_win():
        messagebox.showinfo("Game Over", f"Player {computer} wins!")
        restart_game()
    elif check_draw():
        messagebox.showinfo("Game Over", "It's a draw!")
        restart_game()


def minimax(board, depth, is_maximizing):
    scores = {
        player: -1,
        computer: 1,
        "draw": 0
    }

    if check_win():
        return scores[computer] if is_maximizing else scores[player]
    elif check_draw():
        return scores["draw"]

    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = computer
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score


def reset_board():
    for button in buttons:
        button.config(text=" ", state=tk.NORMAL)


# Create buttons for each position
buttons = []
for i in range(9):
    button = tk.Button(root, text=" ", width=10, height=4, command=lambda index=i: make_move(index))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

# Create restart button
restart_button = tk.Button(root, text="Restart", command=restart_game)
restart_button.grid(row=3, column=0, columnspan=3, pady=10)

# Computer makes the first move
computer_move()

root.mainloop()
