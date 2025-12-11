import time, functools
# def log(func):
#     def wrapper(*args, **kw):
#         print('call %s():' % func.__name__)
#         return func(*args, **kw)
#     return wrapper
  
# @log
# def now():
#     print('2025-04-30')
    
# now()


# 如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数

# def log(text):
#     def decorator(func):
#         @functools.wraps(func) # 不加这句的话 执行now后，now.__name__ 是wrapper，有些依赖函数签名的代码执行就会出错。
#         def wrapper(*args, **kw):
#             print('%s %s():' % (text, func.__name__))
#             return func(*args, **kw)
#         return wrapper
#     return decorator
  
# @log('execute')
# def now():
#     print('2024-6-1')
    
# now()
# print(now.__name__)

def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kw):
        startTime = time.time()
        # 执行一下fn
        result = fn(*args, **kw)
        endTime = time.time()
        print('%s 函数执行一共用了, %s 秒' % (fn.__name__, endTime - startTime))
        return result
    return wrapper
  
# 测试
@metric
def fast(x, y):
    time.sleep(0.0012)
    return x + y

@metric
def slow(x, y, z):
    time.sleep(0.1234)
    return x * y * z

f = fast(11, 22)
s = slow(11, 22, 33)

if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')