# if 判断
# birth = int(input('birth: '))
# if birth < 2000:
#     print('00前')
# else:
#     print('00后')

# 计算BMI

height = 1.75
weight = 80.5

bmi = weight / (height ** 2)

if bmi > 32:
    print('严重肥胖')
elif 28 < bmi <= 32:
    print('肥胖')
elif 25 < bmi <= 28:
    print('过重')
elif 18.5 < bmi <= 25:
    print('正常')
else:
    print('过轻')