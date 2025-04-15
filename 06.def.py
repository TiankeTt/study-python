# 函数

# 内置函数
# abs 绝对值
# num = 100
# abs(num)
# num_fu = -20
# abs(num_fu)

# max
# list = [1, 2, 3, 5]
# print(max(list))

# n1 = 255
# print(hex(n1))

# 自定义函数

# def my_abs(x):
#     if not isinstance(x, (int, float)):
#         raise TypeError('bad operand type')
#     if x >= 0:
#         return x
#     else:
#         return -x
      
# print(my_abs('222'))

# 空函数 pass 算是一个占位符
# def nop():
#     pass

# def power(x, n):
#     return x ** n

# print(power(5, 2))
# print(power(5, 3))

# 给定一组数字a, b, c....，计算a的平方+b的平方+c的平方...

# def clac(numbers):
#     sum = 0
#     for num in numbers:
#         sum += num ** 2
#     return sum

# print(clac((1, 2, 3)))
# print(clac([1, 3, 5, 7]))

# 在 numbers 参数前加一个 *  就可以传入任意参数了。内部会把numbers当做tuple
# def clac(*numbers):
#     sum = 0
#     for num in numbers:
#         sum += num ** 2
#     return sum

# print(clac(1, 2, 3))
# print(clac(1, 3, 5, 7))

# 直接展开了 使用*
# nums = [1, 2, 3]
# print(*nums)

# *kw 类似与 JavaScript中 函数的 args
# **kw 应该是dict这种的

# def person(name, age, **kw):
#     print('name: ', name, 'age: ', age, 'other: ', kw)
    
# person('tianke', 30, 'hhhh', 'mmmm', 'tttt')
# person('Adam', 45, gender='M', job='Engineer')

# def f1(a, b, c=0, *args, **kw):
#     print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

# def f2(a, b, c=0, *, d, **kw):
#     print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)

# f1(1, 2) # a = 1 b = 2 c = 0 args = () kw = {}
# f1(1, 2, c=3) # a = 1 b = 2 c = 3 args = () kw = {}
# f1(1, 2, 3, 'a', 'b') # a = 1 b = 2 c = 3 args = ('a', 'b') kw = {}
# f1(1, 2, 3, 'a', 'b', x=99) # 1 b = 2 c = 3 args = ('a', 'b') kw = {'x': 99}

# def mul(*numbers):
#     if len(numbers) == 0:
#         raise TypeError("mul() missing at least 1 required positional argument")
#     result = 1
#     for num in numbers:
#         result *= num
#     return result

# # 测试
# print('mul(5) =', mul(5))
# print('mul(5, 6) =', mul(5, 6))
# print('mul(5, 6, 7) =', mul(5, 6, 7))
# print('mul(5, 6, 7, 9) =', mul(5, 6, 7, 9))
# if mul(5) != 5:
#     print('mul(5)测试失败!')
# elif mul(5, 6) != 30:
#     print('mul(5, 6)测试失败!')
# elif mul(5, 6, 7) != 210:
#     print('mul(5, 6, 7)测试失败!')
# elif mul(5, 6, 7, 9) != 1890:
#     print('mul(5, 6, 7, 9)测试失败!')
# else:
#     try:
#         mul()
#         print('mul()测试失败!')
#     except TypeError:
#         print('测试成功!')

# 写出 1，3，5， 7 直到 99 的一个list

# L = []
# n = 1
# while n <= 99:
#     L.append(n)
#     n = n+2
# print(L)

# print([i for i in range(1, 100)])