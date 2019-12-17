def get_fuel(mass):
    return mass // 3 - 2

def get_all_fuel(mass):
    total_fuel = 0
    new_fuel = get_fuel(mass)
    while new_fuel > 0:
        total_fuel += new_fuel
        new_fuel = get_fuel(new_fuel)
    return total_fuel

masses = [int(x.strip()) for x in open('../data/input1')]

ans1 = sum(map(get_fuel, masses))

print(ans1)

ans2 = sum(map(get_all_fuel, masses))

print(ans2)