path = input('Путь до файла c числами: ')
with open(path) as file:
    nums_file = file.readlines()
nums = [int(i_num) for i_num in nums_file]
mediana = sorted(nums)[len(nums) // 2]
result = sum(abs(i - mediana) for i in nums)
if result > 20:
    print("20 ходов недостаточно для приведения всех элементов массива к одному числу")
else:
    print(result)
