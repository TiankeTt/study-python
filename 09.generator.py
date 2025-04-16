# 生成器
from functools import reduce

# 惰性计算 生成器 count_up_to 每次只生成一个值，而不是一次性生成所有值。这种方式可以节省内存，特别是在处理大量数据时。
# def count_up_to(n):
#     count = 1
#     while count <= n:
#         yield count
#         count += 1

# # 使用生成器
# for num in count_up_to(5):
#     print(num)

# def fn(x, y):
#     return x * 10 + y
  
# reduce(fn, [1, 3, 5, 7, 9])

def fn(x, y):
    return x * 10 + y

def char2num(s):
    digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    return digits[s]

mapList = map(char2num, '13579')

print(reduce(fn, mapList))