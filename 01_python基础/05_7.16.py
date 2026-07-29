# from random import randint
# # 余额
# balance = randint(0,100)
# # balance = int(input('请输入余额'))
# # 价格
# price = 50
# if balance > price:
#     balance -= price
#     print('余额为',balance,'购买成功，谢谢惠顾')
# else :
#     print('余额不足')
# print('欢迎下次光临')

# match month := 3:
#   case 1 | 3 | 5 | 7 | 8 | 10 | 12:
#     print(f"{month}月有31天")
#   case 4 | 6 | 9 | 11:
#     print(f"{month}月有30天")
#   case 2:
#     print(f"{month}月可能有28天")
#   case _:
#     print(f"{month}月有?天")

# num1 = 2
# num2 = 3
# max_num = num1 if num1 > num2 else num2
# print(max_num)

# rabbit = 2
# week = 1
# while week < 10:
#     rabbit = rabbit + rabbit * 2
#     week += 1
#     print(f"第{week}周有{rabbit}只兔子")

# import time
# 
# num = 1
# while num < 100:
#     print("\r" + "=" * num, end="")
#     num += 1
#     time.sleep(0.05)

# for i in range(-10,10,2):
#     print(i)

# for i in range(1,10):
#     for j in range(1, i + 1):
#         print(f'{i} * {j} = {i * j}',end='\t')
#     print('')

for i in range(10):
    if i % 2 == 0:
        continue
    print(i,end='\t ')