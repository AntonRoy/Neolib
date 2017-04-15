import tqdm
for x in range(660):
    for y in tqdm.tqdm(range(660 - x)):
        for z in range(660 - x - y):
            for b in range(660 - x - y - z):
                if x + y + z + b == 1320:
                    if (x + b == y + z) and (y + b == 2*(x + z)) and (z + b == 3*(x + y)):
                        print('1 = {0}, 2 = {1}, 3 = {2}, Больница = {3}'.format(x, y, z, b))
                        break