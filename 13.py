from intcode import IntCode

tile_map = {
    0: ' ', # blank
    1: '@', # wall
    2: '#', # block
    3: '=', # paddle
    4: 'O', # ball
}

def draw_board(board):
    for j in range(25):
        for i in range(42):
            print(tile_map[board[(i, j)]], end='')
        print()

def update_board(board, outputs):
    for i in range(0, len(outputs), 3):
        x, y, tile = outputs[i:i+3]
        board[(x, y)] = tile

    return board

def get_ball_x(board):
    for k, v in board.items():
        if v == 4:
            return k[0]

def get_paddle_x(board):
    for k, v in board.items():
        if v == 3:
            return k[0]

def get_score(board):
    return board.get((-1, 0))

def get_n_blocks(board):
    return len(list(filter(lambda x: x == 2, board.values())))


code = IntCode.load_from_file('../data/input13')

# part 1
outputs = code.copy().run(print_outputs=False)
board = update_board({}, outputs)
print(get_n_blocks(board))

# part 2
game_code = code.copy()
game_code.code[0] = 2

board = {}
outputs = game_code.run(print_outputs=False)
while not game_code.terminated:
    board = update_board(board, outputs)
    # draw_board(board)
    print("# blocks:", get_n_blocks(board), "\tScore:", get_score(board))

    """
    game logic:
    want to follow ball always.

    v1: -1 if right of ball, 1 if left of ball.
    """
    ball_x, paddle_x = get_ball_x(board), get_paddle_x(board)
    if ball_x < paddle_x:
        inp = -1
    elif ball_x > paddle_x:
        inp = 1
    else:
        inp = 0

    # input()
    # inp = int(input())
    outputs = game_code.run(inputs=[inp], print_outputs=False)

board = update_board(board, outputs)
print("Game finished!")
print("# blocks remaining:", get_n_blocks(board))
print("Final score:", get_score(board))