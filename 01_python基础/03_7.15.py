# num1 = 0.1
# num2 = 0.2
# print(num1 + num2)
#
# from decimal import Decimal
#
# num1 = Decimal('0.1')
# num2 = Decimal('0.2')
# print(num1 + num2)

str1 = """hello world
HELLO WORLD"""
print(str1)

num_int = 123
num_str = "456"
print("num_int 数据类型为:",type(num_int))
print("类型转换前，num_str 数据类型为:",type(num_str))
num_str = int(num_str)
print("类型转换后，num_str 数据类型为:",type(num_str))
num_sum = num_int + num_str
print("num_int 与 num_str 相加结果为:",num_sum)
print("sum 数据类型为:",type(num_sum))
