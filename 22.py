steps = open('../data/input22').readlines()

deck_size = 10007
deck = list(range(deck_size))

for line in steps:
    line = line.strip()
    instr = line.split()

    if instr[0] == 'cut':
        cut_n = int(instr[1])
        deck = deck[cut_n:] + deck[:cut_n]

    elif instr[0] == 'deal' and instr[1] == 'into':
        deck = deck[::-1]

    elif instr[0] == 'deal' and instr[1] == 'with':
        new_deck = [None for _ in range(deck_size)]
        inc = int(instr[-1])

        for i in range(deck_size):
            new_deck[(i*inc) % deck_size] = deck[i]

        deck = new_deck

    # print(deck[:30])

# print(deck)
# print(deck[2020])
print(deck.index(2019))

# part 2

deck_size = 119315717514047
n_iters =   101741582076661
n_iters = 20
start_pos = 2020

# 119315717514047
#  46993733263299
#   3867632483192
# go backwards to find initial position

# find loop
i = 0
pos = start_pos
visited = set()
for i in range(n_iters):
    visited.add(pos)
    for line in steps[::-1]:
        line = line.strip()
        instr = line.split()

        if instr[0] == 'cut':
            cut_n = int(instr[1])

            # forward: + deck_size - n
            pos = (pos + cut_n - deck_size) % deck_size

        elif instr[0] == 'deal' and instr[1] == 'into':
            pos = deck_size - pos - 1

        elif instr[0] == 'deal' and instr[1] == 'with':
            inc = int(instr[-1])

            tmp = pos
            for j in range(inc):
                if tmp % inc == 0:
                    pos = tmp // inc
                    break
                tmp += deck_size
            else:
                raise ValueError
    print(pos)
    # if i % 10000 == 0:
    #     print(i, end='..', flush=True)

    # if pos in visited:
    #     print("returned to previous location after {} iterations".format(i))
    # if pos == start_pos:
    #     print("loops after {} iterations".format(i))
    #     break


print(pos)