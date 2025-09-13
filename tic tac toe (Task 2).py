import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Human Vs AI")

board = [" " for _ in range(9)]  
buttons = []  

wins = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

def check_winner(player):
    for combo in wins:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return combo
    return None

def minimax(board, is_maximizing):
    if check_winner("X"):
        return 1
    if check_winner("O"):
        return -1
    if " " not in board:
        return 0

    if is_maximizing:
        best_score = -999
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, False)
                board[i] = " "
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = 999
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, True)
                board[i] = " "
                best_score = min(best_score, score)
        return best_score

def flash_button(index, color, times=4, delay=200, callback=None):
    """Flash a button with animation effect"""
    def toggle(count):
        if count > 0:
            current = buttons[index].cget("bg")
            buttons[index].config(bg=color if current == "SystemButtonFace" else "SystemButtonFace")
            root.after(delay, toggle, count - 1)
        else:
            buttons[index].config(bg="SystemButtonFace")
            if callback:
                callback()
    toggle(times)

def ai_move():
    best_score = -999
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    if move is not None:
        # AI animation: flash before placing "X"
        flash_button(move, "lightblue", times=3, delay=200, callback=lambda: place_ai(move))

def place_ai(move):
    board[move] = "X"
    buttons[move].config(text="X", state="disabled")
    winner_combo = check_winner("X")
    if winner_combo:
        animate_winner(winner_combo, "red", "Lost, Gotta use more brain!")
    elif " " not in board:
        messagebox.showinfo("Game Over", "Not Bad!")
        reset_game()

def on_click(i):
    if board[i] == " ":
        board[i] = "O"
        buttons[i].config(text="O", state="disabled")
        winner_combo = check_winner("O")
        if winner_combo:
            animate_winner(winner_combo, "green", "You Win!")
        elif " " not in board:
            messagebox.showinfo("Game Over", "Not Bad!")
            reset_game()
        else:
            ai_move()

def animate_winner(combo, color, message):
    """Flash winning cells and show message"""
    def flash_winner(count=6):
        if count > 0:
            for idx in combo:
                current = buttons[idx].cget("bg")
                buttons[idx].config(bg=color if current == "SystemButtonFace" else "SystemButtonFace")
            root.after(300, flash_winner, count - 1)
        else:
            messagebox.showinfo("Game Over", message)
            reset_game()
    flash_winner()

def reset_game():
    global board
    board = [" " for _ in range(9)]
    for btn in buttons:
        btn.config(text=" ", state="normal", bg="SystemButtonFace")

# Create grid buttons
for i in range(9):
    btn = tk.Button(root, text=" ", font=("Arial", 24), width=5, height=2,
                    command=lambda i=i: on_click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

root.mainloop()
