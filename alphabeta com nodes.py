
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


def print_board(grid):
    for i in range(0, len(grid)):
        print(grid[i])
@count_calls
def minimaxAB(grid, player, depth, alpha, beta):
    if depth == 0 or detect_win(grid):
        return calculate_score(grid), None
    if player == 2:
        best_score = -float("inf")
        best_col = None
        for col in range(len(grid[0])):
            if is_valid_move(grid, col):
                child = make_move(grid, col, player)
                score, _ = minimaxAB(child, 1, depth - 1, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_col = col
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score, best_col
    else:
        best_score = float("inf")
        best_col = None
        for col in range(len(grid[0])):
            if is_valid_move(grid, col):
                child = make_move(grid, col, player)
                score, _ = minimaxAB(child, 2, depth - 1, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_col = col
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
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
    _, col = minimaxAB(grid, 2, depth,-float("inf"), float("inf"))
    return col


def calculate_score(grid):
    score = 0
    if (detect_win(grid) == 1): score -= 512
    if (detect_win(grid) == 2): score += 512
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if j <= len(grid[i]) - 4:

                line = [grid[i][j], grid[i][j + 1], grid[i][j + 2], grid[i][j + 3]]
                score += get_line_score(line)
            if i <= len(grid) - 4:
                line = [grid[i][j], grid[i + 1][j], grid[i + 2][j], grid[i + 3][j]]
                score += get_line_score(line)
            if i <= len(grid) - 4 and j <= len(grid[i]) - 4:

                line = [grid[i][j], grid[i + 1][j + 1], grid[i + 2][j + 2], grid[i + 3][j + 3]]
                score += get_line_score(line)
            if i <= len(grid) - 4 and j >= 3:

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
        bestValue = max(bestValue, minimaxAB(i, 2, False, lastpiece,-float("inf"), float("inf")))
        if (bestValue == minimaxAB(i, 2, False, lastpiece,-float("inf"), float("inf"))):
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


def play_game():
    grid = [[0, 0, 0, 0, 0, 0, 0],  # 0
            [0, 0, 0, 0, 0, 0, 0],  # 1
            [0, 0, 0, 0, 0, 0, 0],  # 2
            [0, 0, 0, 0, 0, 0, 0],  # 3
            [0, 0, 0, 0, 0, 0, 0],  # 4
            [0, 0, 0, 0, 0, 0, 0]]  # 5
    print_board(grid)
    print("----------------------------")
    while (detect_win(grid) == 0 and count_zeros(grid) > 0):
        print("Player 1")
        c = input('column?\n')
        grid = movement(grid, int(c) - 1, 2)
        print_board(grid)
        print("----------------------------")
        if (detect_win(grid) == 1):
            print("Player 1 wins")
            break
        print("Player 2")
        c = input('column?\n')
        grid = movement(grid, int(c) - 1, 1)
        print_board(grid)
        print("----------------------------")
        if (detect_win(grid) == 2):
            print("Player 2 wins")
            break
    if (detect_win(grid) == 0):
        print("Draw")


def play_minimax():
    grid = [[0, 0, 0, 0, 0, 0, 0],  # 0
            [0, 0, 0, 0, 0, 0, 0],  # 1
            [0, 0, 0, 0, 0, 0, 0],  # 2
            [0, 0, 0, 0, 0, 0, 0],  # 3
            [0, 0, 0, 0, 0, 0, 0],  # 4
            [0, 0, 0, 0, 0, 0, 0]]  # 5
    print_board(grid)
    print("----------------------------")
    while (detect_win(grid) == 0 and count_zeros(grid) > 0):
        print("Player 1")
        c = input('column?\n')
        grid = movement(grid, int(c) - 1, 2)
        print_board(grid)
        print("----------------------------")
        if (detect_win(grid) == 1):
            print("Player 1 wins")
            break
        print("MinimaxAB")
        c = minimaxAB(grid, 1, 4,-float("inf"), float("inf"))
        grid = movement(grid, get_best_move(grid, 4), 1)
        print_board(grid)
        print(minimaxAB.count)
        print("----------------------------")
        if (detect_win(grid) == 2):
            print("Player 2 wins")
            break
    if (detect_win(grid) == 0):
        print("Draw")

def count_zeros(grid):
    count = 0
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if (grid[i][j] == 0):
                count += 1
    return count


best_move = None
best_value = -1000


play_minimax()

