def result_circular_array_m(n, m):
    yield 1
    for i in range(m - 1, n * m, m - 1):
        stop = i % n + 1
        if stop == 1: return
        yield stop


n = int(input("Ввидите сколько чисел должно быть в массиве:"))
m = int(input("Ввидите число длинны обхода массива:"))
massiv = [i_mass for i_mass in range(1, n + 1)]
print(f'Круговой массив:{''.join(str(i_massiv) for i_massiv in massiv)}')
result = list(result_circular_array_m(n, m))
print(''.join(str(i_number) for i_number in result))

