# names = ['Michael', 'Bob', 'Tracy']
# for name in names:
#     print(name)

# sum = 0
# for x in range(101):
#     sum = sum + x
# print(sum)

# sum = 0
# n = 99
# while n > 0:
#     sum = sum + n
#     n = n - 2
# print(sum)

# L = ['Bart', 'Lisa', 'Adam']

# for name in L:
#     print('Hello, ',name)

# 查找list最大最小值
# def findMinAndMax(L):
#         if len(L) == 0:
#                 return (None, None)
#         return (min(L), max(L))

def findMinAndMax(L):
        if len(L) == 0:
            return (None, None)
        min = L[0]
        max = L[0]
        for x in L:
            if x < min:
                min = x
            elif x > max:
                max = x
        return (min, max)

# 测试
if findMinAndMax([]) != (None, None):
    print('测试失败!')
elif findMinAndMax([7]) != (7, 7):
    print('测试失败!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('测试失败!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('测试失败!')
else:
    print('测试成功!')