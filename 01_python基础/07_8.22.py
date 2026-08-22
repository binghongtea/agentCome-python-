# def printXint(row,col):
#     while row > 0:
#         print('*' * col)
#         row -= 1
#     print('-' * 50)
# 
# printXint(1,2)
# printXint(2,3)
# printXint(3,4)

# def printInfo1(num1,*cc,num) :
#     print(num)
#     print(num1)
#     print(cc)
#
# printInfo1(1,2,3,4,num=1)
#
# def printInfo(num,**vardict):
#   print(num)
#   print(vardict)
#   # return
#
# printInfo(10,key1 = 20,key2 = 30)
# printInfo(10,a = 20,b = 30)

# import copy
#
# def multiply(var1):
#     var1[3].append(400)
#     print(var1)
#
# list1 = [1, 2, 3,[1,3]]
# print(list1)
# multiply(copy.deepcopy(list1))
# print(list1)

# def adult(age=18):
#     """根据年龄判断是否成年"""
#     result = "未成年"[age >= 18 :]
#     print(result)
#
# help(adult)

# def jiecheng(num):
#     if (num > 1):
#         return num * jiecheng(num - 1)
#     else :
#         return 1

# def jiecheng(num):
#     return num * jiecheng(num - 1) if num > 1 else 1
#
# print(jiecheng(6))

# def dog(name:str,age:(1,999),type:'狗的类型'):
#     print(name,age,type)
#
# print(dog.__annotations__)