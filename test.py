offspring = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10
]

for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
    print(ind1, ind2)


a = [
    1, 2, 3, 4, 5, 6, 7
]

b = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10
]

for x, y in zip(a, b):
    print(x, y)
