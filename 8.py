# solution without numpy

from collections import Counter
from itertools import product

width = 25
height = 6

pixels = [
    int(x)
    for x in open('../data/input8').read().strip()
]

def read_layers(pixels, width, height):
    layers = []
    layer = []
    row = []
    for pix in pixels:
        row.append(pix)
        if len(row) == width:
            layer.append(row)
            row = []
            if len(layer) == height:
                layers.append(layer)
                layer = []

    return layers

layers = read_layers(pixels, width*height, 1)

layer_counts = []
min_zero = None
for layer in layers:
    layer_counts.append(Counter(layer[0]))

    n_zero = layer_counts[-1][0]
    if min_zero is None or n_zero < min_zero:
        min_zero = n_zero

for lc in layer_counts:
    if lc[0] == min_zero:
        print(lc[1] * lc[2])
        break

# part 2
layers = read_layers(pixels, width, height)

image = [[None for _ in range(width)] for _ in range(height)]
for i, j in product(range(height), range(width)):
    for layer in layers:
        if layer[i][j] != 2:
            image[i][j] = layer[i][j]
            break

for row in image:
    print(''.join([str(x) for x in row]))
