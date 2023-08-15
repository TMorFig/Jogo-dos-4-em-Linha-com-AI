import tkinter as tk
import time

def count_calls(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        return func(*args, **kwargs)
    wrapper.count = 0
    return wrapper

def movimento(grid, j):
    for i in range(0, len(grid)):
        if (i == len(grid) - 1 and grid[i][j] == 0):
            grid[i][j] = 1
            return grid
        else:
            if ((grid[i][j] == 0 and grid[i + 1][j] != 0)):
                grid[i][j] = 1
                return grid
    return grid


def movement(grid, j, lastpiece):
    if (lastpiece == 2):
        grid1 = [row[:] for row in grid]
        i = 0
        while (grid1[i][j] == 0):
            i += 1
            if (i == len(grid1)):
                # grid[i][j]=1
                break
        grid1[i - 1][j] = 1
        return grid1
    if (lastpiece == 1):
        grid1 = [row[:] for row in grid]
        i = 0
        while (grid1[i][j] == 0):
            i += 1
            if (i == len(grid1)):
                # grid[i][j]=1
                break
        grid1[i - 1][j] = 2
        return grid1


def successors(grid, lastpiece):
    if (lastpiece == 1):
        lista = []
        grid3 = [row[:] for row in grid]
        for j in range(0, len(grid[0])):
            grid2 = [row[:] for row in grid]
            lista.append(movement(grid2, j, 1))
            # backwards_movement(grid,j)
        return lista
    if (lastpiece == 2):
        lista = []
        grid3 = [row[:] for row in grid]
        for j in range(0, len(grid[0])):
            grid2 = [row[:] for row in grid]
            lista.append(movement(grid2, j, 2))
            # backwards_movement(grid,j)
        return lista

@count_calls
def minimax(grid, player, depth):
    if depth == 0 or detect_win(grid):
        return calculate_score(grid), None
    if player == 2:
        best_score = -float("inf")
        best_col = None
        for col in range(len(grid[0])):
            if is_valid_move(grid, col):
                child = make_move(grid, col, player)
                score, _ = minimax(child, 1, depth - 1)
                if score > best_score:
                    best_score = score
                    best_col = col
        return best_score, best_col
    else:
        best_score = float("inf")
        best_col = None
        for col in range(len(grid[0])):
            if is_valid_move(grid, col):
                child = make_move(grid, col, player)
                score, _ = minimax(child, 2, depth - 1)
                if score < best_score:
                    best_score = score
                    best_col = col

        return best_score, best_col


def is_valid_move(grid, col):
    return grid[0][col] == 0


def make_move(grid, col, player):
    new_grid = [row[:] for row in grid]
    for row in range(len(new_grid) - 1, -1, -1):
        if new_grid[row][col] == 0:
            new_grid[row][col] = player
            break
    return new_grid


def get_best_move(grid, depth):
    _, col = minimax(grid, 2, depth)
    return col


def calculate_score(grid):

    score = 0
    if (detect_win(grid) == 1): score -= 512
    if (detect_win(grid) == 2): score += 512
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if j <= len(grid[i]) - 4:
                # check horizontal line
                line = [grid[i][j], grid[i][j + 1], grid[i][j + 2], grid[i][j + 3]]
                score += get_line_score(line)
            if i <= len(grid) - 4:
                # check vertical line
                line = [grid[i][j], grid[i + 1][j], grid[i + 2][j], grid[i + 3][j]]
                score += get_line_score(line)
            if i <= len(grid) - 4 and j <= len(grid[i]) - 4:
                # check diagonal line (top left to bottom right)
                line = [grid[i][j], grid[i + 1][j + 1], grid[i + 2][j + 2], grid[i + 3][j + 3]]
                score += get_line_score(line)
            if i <= len(grid) - 4 and j >= 3:
                # check diagonal line (top right to bottom left)
                line = [grid[i][j], grid[i + 1][j - 1], grid[i + 2][j - 2], grid[i + 3][j - 3]]
                score += get_line_score(line)
    return score


def get_line_score(line):

    count_ones = line.count(1)
    count_twos = line.count(2)
    if count_ones == 3 and count_twos == 0:
        return -50
    elif count_ones == 2 and count_twos == 0:
        return -10
    elif count_ones == 1 and count_twos == 0:
        return -1
    elif count_ones == 0 and count_twos == 0:
        return 0
    elif count_twos == 1 and count_ones == 0:
        return 1
    elif count_twos == 2 and count_ones == 0:
        return 10
    elif count_twos == 3 and count_ones == 0:
        return 50
    else:
        return 0


def best_move(grid, lastpiece):
    bestValue = -1000
    for i in successors(grid, lastpiece):
        bestValue = max(bestValue, minimax(i, 2, False, lastpiece))
        if (bestValue == minimax(i, 2, False, lastpiece)):
            best_move = i
    return best_move


def detect_win(grid):
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if (grid[i][j] == 1):
                if (i < len(grid) - 3):
                    if (grid[i + 1][j] == 1 and grid[i + 2][j] == 1 and grid[i + 3][j] == 1):
                        return 1
                if (j < len(grid[0]) - 3):
                    if (grid[i][j + 1] == 1 and grid[i][j + 2] == 1 and grid[i][j + 3] == 1):
                        return 1
                if (i < len(grid) - 3 and j < len(grid[0]) - 3):
                    if (grid[i + 1][j + 1] == 1 and grid[i + 2][j + 2] == 1 and grid[i + 3][j + 3] == 1):
                        return 1
                if (i < len(grid) - 3 and j > 2):
                    if (grid[i + 1][j - 1] == 1 and grid[i + 2][j - 2] == 1 and grid[i + 3][j - 3] == 1):
                        return 1
            if (grid[i][j] == 2):
                if (i < len(grid) - 3):
                    if (grid[i + 1][j] == 2 and grid[i + 2][j] == 2 and grid[i + 3][j] == 2):
                        return 2
                if (j < len(grid[0]) - 3):
                    if (grid[i][j + 1] == 2 and grid[i][j + 2] == 2 and grid[i][j + 3] == 2):
                        return 2
                if (i < len(grid) - 3 and j < len(grid[0]) - 3):
                    if (grid[i + 1][j + 1] == 2 and grid[i + 2][j + 2] == 2 and grid[i + 3][j + 3] == 2):
                        return 2
                if (i < len(grid) - 3 and j > 2):
                    if (grid[i + 1][j - 1] == 2 and grid[i + 2][j - 2] == 2 and grid[i + 3][j - 3] == 2):
                        return 2
    return 0



def count_zeros(grid):
    count = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if (grid[i][j] == 0):
                count += 1
    return count


def button_click(column):
    global current_player,board
    for row in range(5, -1, -1):
        if board[row][column] == 0:
            board[row][column] = 1
            update_board()
            a = minimax.count

            start_time = time.time()
            board = movement(board, get_best_move(board, 4), 1)
            end_time = time.time()

            update_board()
            if detect_win(board) == 1:
                disable_buttons()
                message.config(text=f"YOU WIN!")
                break
            if detect_win(board) == 2:
                disable_buttons()
                message.config(text=f"YOU LOSE! GAME OVER !")
                break

            current_player = 3 - current_player
            execution_time = end_time - start_time
            message_text = f"Total nodes explored= {minimax.count-a}                                                          Time = {execution_time:.3f} seconds"
            message.config(text=message_text)
            message.pack()
            break

# Define the function to update the board display
def update_board():
    for row in range(6):
        for column in range(7):
            if board[row][column] == 0:
                canvas.itemconfig(buttons[row][column], fill="white")
            elif board[row][column] == 1:
                canvas.itemconfig(buttons[row][column], fill="red")
            elif board[row][column] == 2:
                canvas.itemconfig(buttons[row][column], fill="yellow")

# Define the function to draw a circle on a canvas
def draw_circle(canvas, x, y, r, **kwargs):
    return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)


# Define the function to disable all the circular buttons
def disable_buttons():
    for row in range(6):
        for column in range(7):
            canvas.itemconfig(buttons[row][column], state="disabled")
def enable_buttons():
    for row in range(6):
        for column in range(7):
            canvas.itemconfig(buttons[row][column], state="normal")

# Define the function to restart the game
def restart_game():
    global board, current_player
    board = [[0 for _ in range(7)] for _ in range(6)]
    update_board()
    for row in range(6):
        for column in range(7):
            canvas.itemconfig(buttons[row][column], state="normal")
    current_player = 1
    message.config(text="")

best_move = None
best_value = -1000
# Create the main window
root = tk.Tk()
root.title("4 em linha com MinMax")

# Create the message widget
message = tk.Label(root, text="")
message.pack()

board = [[0, 0, 0, 0, 0, 0, 0],  # 0
            [0, 0, 0, 0, 0, 0, 0],  # 1
            [0, 0, 0, 0, 0, 0, 0],  # 2
            [0, 0, 0, 0, 0, 0, 0],  # 3
            [0, 0, 0, 0, 0, 0, 0],  # 4
            [0, 0, 0, 0, 0, 0, 0]]  # 5


# Create the restart button
restart_button = tk.Button(root, text="Restart Game", command=restart_game)
restart_button.pack()

# Create the canvas for the game board
canvas = tk.Canvas(root, width=550, height=490, bg="pink")
canvas.pack()

# Create the buttons as circles on the canvas
buttons = []
button_radius = 30
for row in range(6):
    button_row = []
    for column in range(7):
        x = button_radius + column * (button_radius * 2 + 22)
        y = button_radius + row * (button_radius * 2 + 23)
        button = draw_circle(canvas, x, y, button_radius-4, fill="white", outline="black", width=2)
        canvas.tag_bind(button, "<Button-1>", lambda event, col=column: button_click(col))
        button_row.append(button)
    buttons.append(button_row)

# Initialize the current player to 1 (red)
current_player = 1


# Start the main event loop
root.mainloop()


