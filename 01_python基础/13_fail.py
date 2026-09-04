# while True:
#     print('study')

# print(var1)

# def tryFun():
#     try:
#         result = 3 / 1
#     except ZeroDivisionError as e:
#         print(e)
#     except ValueError as e:
#         print(e)
#     except:
#         print('hhhh')
#     else:
#         print(f'result是{result}')
#     finally:
#         print('结束啦')
#
# tryFun()

# def int_add(a,b):
#     if isinstance(a,int) and isinstance(b,int):
#         return a+b
#     else:
#         raise TypeError('类型错误')

# def int_add(a,b):
#     assert isinstance(a,int) and isinstance(b,int), '参数类型错误'
#     return a+b
#
#
# print(int_add(1,2))
# print(int_add('1','2'))\

# class Myerror(Exception):
#     def __init__(self, value):
#         self.value = value
#
#     def __str__(self):
#         return repr(self.value)
#
# try:
#     raise Myerror(1)
# except Myerror as e:
#     print(e)

with open('test.txt','r') as f:
    print(f.read())
print(f.closed)