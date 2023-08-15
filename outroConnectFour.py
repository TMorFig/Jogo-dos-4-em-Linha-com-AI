import tkinter as tk
# Create the main window
root = tk.Tk()
root.title("4 em linha")

# Create the message widget
message = tk.Label(root, text="")
message.pack()

grid = [[0, 0, 0, 0, 0, 0, 0],  # 0
            [0, 0, 0, 0, 0, 0, 0],  # 1
            [0, 0, 0, 0, 0, 0, 0],  # 2
            [0, 0, 0, 0, 0, 0, 0],  # 3
            [0, 0, 0, 0, 0, 0, 0],  # 4
            [0, 0, 0, 0, 0, 0, 0]]  # 5

board = grid
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


def button_click(column):
    global current_player
    for row in range(5, -1, -1):
        if board[row][column] == 0:
            board[row][column] = current_player
            update_board()
            if detect_win(grid) == 1:
                disable_buttons()
                message.config(text=f"you win!")
                break

            current_player = 3 - current_player
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

