
with open('input') as f:
    data = f.read().strip().split('\n')

def trees_in_slope(right, down, data):
    x = 0
    y = 0
    trees = 0
    while True: 
        x = (right + x) % len(data[0]) 
        y = down + y
        try:
            space = data[y][x]
            if space == '#':
                trees += 1
        except IndexError:
            return trees

total = 1
for x in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    total *= trees_in_slope(x[0], x[1], data)
print(total)

