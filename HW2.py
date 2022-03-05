from matplotlib import pyplot as plt
from time import time


def read_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        data_ = {}
        for line in f:
            address, *raw = line.strip().split('\t')
            data_[address] = list(map(float, raw)) + [0]
    return data_


def dist(x0, x, y0, y):
    return ((x - x0) ** 2 + (y - y0) ** 2) ** 0.5


def task1(data_):
    for i in data_.keys():
        x, y = data_[i][0], data_[i][1]
        for j in data_.keys():
            if dist(x, data_[j][0], y, data_[j][1]) <= 0.5 and i != j:
                data_[i][3] += 1
    best_place_ = sorted([i[3] for i in data_.values()])[-1]
    for i in data_.keys():
        if data_[i][3] == best_place_:
            best_place_ = data_[i][0], data_[i][1]
    return best_place_


def task2(data_):
    to_sort = set(sorted([i[3] for i in data_.values()]))
    top = []
    for i in to_sort:
        for j in data_.keys():
            if data_[j][3] == i:
                top.append([data_[j][0], data_[j][1], i])
    for i in range(len(top)):
        for j in range(len(top)):
            if dist(top[i][0], top[j][0], top[i][1], top[j][1]) <= 1 and top[i][2] >= top[j][2] and top[i] != top[j]:
                top[j] = [0, 0, 0]
    top_10_ = []
    for i in top:
        if i != [0, 0, 0]:
            top_10_.append(i)
    top_10_ = tuple([(i[0],i[1]) for i in top_10_][-10::])
    return top_10_


def tenants(area):
    return (area*0.7)/18


def task3(data_):
    for i in data_.keys():
        data_[i][2] = tenants(data_[i][2])
        for j in data_.keys():
            if dist(data_[i][0],data_[j][0],data_[i][1],data_[j][1]) <= 0.5 and i != j:
                data_[i][2] += tenants(data_[j][2])
    to_sort = sorted([i[2] for i in data_.values()])
    top = []
    for i in to_sort:
        for j in data_.values():
            if i == j[2]:
                top.append([j[0],j[1],j[2]])
    top = top[::-1]
    checked_addresses = []
    checked_addresses.append(top[0])
    print(checked_addresses)
    for i in top:
        count = 0
        for j in checked_addresses:
            if dist(i[0], j[0], i[1], j[1]) > 1:
                count += 1
        if count == len(checked_addresses):
            checked_addresses.append(i)
    print(checked_addresses)
    checked_addresses = [(i[0],i[1]) for i in checked_addresses]
    return checked_addresses[0:16:]#addresses[len(addresses)-16:len(addresses)+1:1]

def plot(database, best_coords):
    plt.close()
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.plot([coord[0] for coord in database.values()],
             [coord[1] for coord in database.values()], '.', ms=5, color='k', alpha=0.5)
    if isinstance(best_coords[0], tuple):
        for x, y in best_coords:
            circle = plt.Circle((x, y), 0.5, color='r', fill=False, zorder=2)
            ax.add_patch(circle)
        plt.plot([coord[0] for coord in best_coords],
                 [coord[1] for coord in best_coords], '.', ms=15, color='r')
    elif isinstance(best_coords[0], float):
        x, y = best_coords
        circle = plt.Circle((x, y), 0.5, color='r', fill=False, zorder=2)
        ax.add_patch(circle)
        plt.plot(*best_coords, '.', ms=15, color='r')
    else:
        raise ValueError("Проверь, что подаёшь список кортежей или кортеж из двух координат")
    plt.show()


def homework():
    path = "buildings.txt"
    database = read_data(path)

    best_task1 = task1(database)
    plot(database, best_task1)

    top10_task2 = task2(database)
    plot(database, top10_task2)

    top15_task2 = task3(database)
    plot(database, top15_task2)


if __name__ == '__main__':
    time1 = time()
    homework()
    time2 = time()
    print(time2 - time1)