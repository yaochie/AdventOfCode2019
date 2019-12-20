from pprint import pprint
from collections import Counter, defaultdict
import math
import time

import tests.t14 as t14

def parse_chem(s):
    quantity, chem = s.strip().split()
    return int(quantity), chem

def read_reaction(line):
    inputs, output = line.strip().split('=>')
    inputs = [
        parse_chem(s)
        for s in inputs.split(', ')
    ]
    output = parse_chem(output)

    return inputs, output

reactions = open('../data/input14').readlines()

# reactions = t14.reactions_5

reactions = [read_reaction(line) for line in reactions]

# no chemical appears more than once in the output, so we can just
# count backwards from FUEL

# map outputs to inputs
reaction_map = {}
for inputs, (q, chem) in reactions:
    if chem in reaction_map:
        raise ValueError
    reaction_map[chem] = {'quantity': q, 'inputs': inputs}

# pprint(reaction_map)

def all_done(to_make):
    for chem, q in to_make.items():
        if chem != 'ORE' and q > 0:
            return False

    return True

def calculate_ore(fuel):
    to_make = defaultdict(int)
    to_make['FUEL'] = fuel
    while not all_done(to_make):
        # find chemical to make that only requires chemicals not in the list of chemicals to make
        # print(to_make)
        change = False
        for chem, q in to_make.items():
            if chem == 'ORE' or q <= 0:
                continue

            reaction = reaction_map[chem]
            good = True
            for _, inp_chem in reaction['inputs']:
                if inp_chem != 'ORE' and inp_chem in to_make and to_make[inp_chem] > 0:
                    good = False
                    break

            if not good:
                continue

            # print(f"making {q} {chem}")
            n_reactions = math.ceil(q / reaction['quantity'])

            for inp_q, inp_chem in reaction['inputs']:
                to_make[inp_chem] += inp_q * n_reactions

            # subtract extra?
            n_made = n_reactions * reaction['quantity']
            to_make[chem] -= n_made
            change = True
            break

        if not change:
            print("Nothing changed!")
            raise ValueError

    return to_make['ORE']

ans_1 = calculate_ore(1)
print("Part 1:", ans_1)

# part 2

# attempt 1: iteration until more than 1e12 (will take > 50 min)
# attempt 2: search for the amount of starting fuel?

n_ore = 1000000000000

# find an upper and lower limit
max_fuel = 1
while True:
    ore_used = calculate_ore(max_fuel)
    print(f"{max_fuel:>12d} FUEL requires {ore_used:>13d} ORE")
    if ore_used > n_ore:
        min_fuel = max_fuel // 2
        break

    max_fuel *= 2

print(f'Range: {min_fuel} - {max_fuel}')

# binary search/linear search
while True:
    if max_fuel - min_fuel == 1:
        print("Part 2:", min_fuel)
        break

    guess = (max_fuel + min_fuel) // 2
    ore_used = calculate_ore(guess)
    print(f"{guess:>12d} FUEL requires {ore_used:>13d} ORE")
    if ore_used > n_ore:
        max_fuel = guess
    elif guess == n_ore:
        print("Part 2:", guess)
        break
    else:
        min_fuel = guess

    # print(f'Range: {min_fuel} - {max_fuel}')
