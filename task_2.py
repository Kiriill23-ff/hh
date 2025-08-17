from math import sqrt

path_1 = input('Путь до файла с координатами и радиусом окружности: ')
path_2 = input('Путь до файла с координатами точек: ')
with open(path_1) as file_1:
    x_1, y_1 = file_1.readline().split()
    x_1, y_1 = float(x_1), float(y_1)
    r = int(file_1.readline(2))
with open(path_2) as file_2:
    points = file_2.readlines()
for point in points:
    x = float(point.split()[0])
    y = float(point.split()[1])
    r_with_center_x_y = sqrt((x_1 - x) ** 2 + (y_1 - y) ** 2)
    if r_with_center_x_y == r:
        print("0 - точка лежит на окружности")
    elif r_with_center_x_y < r:
        print("1 - точка внутри")
    else:
        print("2 - точка снаружи")
