import itertools

def read_board(lines):
    board = {}
    for i, line in enumerate(lines):
        for j, value in enumerate(line.strip()):
            board[(i, j)] = value == '#'

    return board

def biodiversity_rating(board_dict):
    flat_board = [board_dict[(i, j)] for i in range(5) for j in range(5)]

    ratings = [int(x) * (2 ** i) for i, x in enumerate(flat_board)]
    return sum(ratings)

def draw_board(board_dict):
    for i in range(5):
        for j in range(5):
            if (i, j) == (2, 2):
                char = '?'
            else:
                char = '#' if board_dict[(i, j)] else '.'
            print(char, end='')
        print()

def hash_board(board_dict):
    flat_board = [board_dict[(i, j)] for i in range(5) for j in range(5)]
    return ''.join(str(int(x)) for x in flat_board)

def update_board(board):
    new_board = {}
    for i, j in itertools.product(range(5), repeat=2):
        neighbors = [
            (i-1, j),
            (i+1, j),
            (i, j-1),
            (i, j+1)
        ]

        n_bugs = 0
        for nb in neighbors:
            if nb in board and board[nb]:
                n_bugs += 1

        if (not board[(i, j)]) and (n_bugs == 1 or n_bugs == 2):
            new_board[(i, j)] = True
        elif board[(i, j)] and n_bugs == 1:
            new_board[(i, j)] = True
        else:
            new_board[(i, j)] = False

    return new_board


start = open('../data/input24').readlines()

# start = """....#
# #..#.
# #..##
# ..#..
# #....""".splitlines()

start_board = read_board(start)

board = start_board

seen_boards = set()
seen_boards.add(hash_board(board))
while True:
    new_board = update_board(board)
    
    if hash_board(new_board) in seen_boards:
        print(biodiversity_rating(new_board))
        break

    board = new_board
    seen_boards.add(hash_board(board))


# part 2

def empty_board():
    return {(i, j): False for i, j in itertools.product(range(5), repeat=2)}

inside_border = [
    (1, 2),
    (2, 1),
    (3, 2),
    (2, 3),
]

def update_board_v2(board, board_inside, board_outside):
    new_board = {}
    for i, j in itertools.product(range(5), repeat=2):
        if (i, j) == (2, 2):
            continue

        elif (i, j) in inside_border:
            n_bugs = 0
            if (i, j) == (1, 2):
                n_bugs += sum(int(board_inside[(0, y)]) for y in range(5))
            elif (i, j) == (2, 1):
                n_bugs += sum(int(board_inside[(x, 0)]) for x in range(5))
            elif (i, j) == (3, 2):
                n_bugs += sum(int(board_inside[(4, y)]) for y in range(5))
            elif (i, j) == (2, 3):
                n_bugs += sum(int(board_inside[(x, 4)]) for x in range(5))
            else:
                raise ValueError

            neighbors = [
                (i-1, j),
                (i+1, j),
                (i, j-1),
                (i, j+1)
            ]

            n_bugs += sum(int(board[nb]) for nb in neighbors if nb != (2, 2))

        elif i == 0 or i == 4 or j == 0 or j == 4:
            n_bugs = 0

            if i == 0:
                n_bugs += int(board_outside[(1, 2)])
            if i == 4:
                n_bugs += int(board_outside[(3, 2)])
            if j == 0:
                n_bugs += int(board_outside[(2, 1)])
            if j == 4:
                n_bugs += int(board_outside[(2, 3)])

            neighbors = [
                (i-1, j),
                (i+1, j),
                (i, j-1),
                (i, j+1)
            ]

            n_bugs += sum(int(board[nb]) for nb in neighbors if nb in board)

        else:
            n_bugs = 0
            neighbors = [
                (i-1, j),
                (i+1, j),
                (i, j-1),
                (i, j+1)
            ]

            n_bugs = sum(int(board[nb]) for nb in neighbors)

        if (not board[(i, j)]) and (n_bugs == 1 or n_bugs == 2):
            new_board[(i, j)] = True
        elif board[(i, j)] and n_bugs == 1:
            new_board[(i, j)] = True
        else:
            new_board[(i, j)] = False

    return new_board

def bug_sum(board):
    return sum(int(v) for v in board.values())

start = open('../data/input24').readlines()

# start = """....#
# #..#.
# #..##
# ..#..
# #....""".splitlines()

start_board = read_board(start)

n_iters = 200

all_boards = {i: empty_board() for i in range(-n_iters-1, n_iters+2)}
all_boards[0] = start_board

# for k, v in all_boards.items():
#     print("Depth", k)
#     draw_board(all_boards[k])
# print()
# print("-----------------")
# print()

for i in range(1, n_iters+1):
    print(i, end='..', flush=True)
    all_new_boards = {j: empty_board() for j in range(-n_iters-1, n_iters+2)}
    for k in range(-i, i+1):
        all_new_boards[k] = update_board_v2(all_boards[k], all_boards[k+1], all_boards[k-1])
    
    all_boards = all_new_boards

# for k, v in all_boards.items():
#     print("Depth", k)
#     draw_board(all_boards[k])
# print()
# print("-----------------")
# print()

# sum all bugs
print()
print("Bug sum:", sum(bug_sum(board) for board in all_new_boards.values()))