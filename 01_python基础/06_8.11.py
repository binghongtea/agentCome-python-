# sum = 0
# for i in range(10):
#     sum += i**i
#     if sum > 100000:
#         print(sum,i)
#         break
#     else :
#         print(sum,i)

# list1 = [1, 2, 3]
# print(list1)
# list1.append(4)
# print(list1)
# print(list1[0:])
# list1.insert(1, 5)
# print(list1)

# list1 = [100, 200, 300, 400, 500]
# print(enumerate(list1))
# for i, val in enumerate(list1):
#     print(i, val)

# list1 = [100, 200, 300, 400, 500]
# del list1[2]
# print(list1)

# list1 = [1, 2, 3, 4, 5]
# list2 = ["a", "b", "c", "d", "e"]
# tuple_list = [(i, j) for i in list1 for j in list2]
# print(tuple_list)
#
# list1 = [1, 2, 3, 4, 5]
# list2 = ["a", "b", "c", "d", "e"]
# zipped = zip(list1, list2)
# print(list(zipped))

# str1 = "hello world"
# print(str1[0])
# print(str1[-1])
# print(str1[4:-3])
#
# print("hello\nworld")
# print(r"hello\nworld")
#
# tuple_generator = (x for x in range(10))  # 获取生成器对象
# print(tuple_generator)
# tuple1 = tuple(tuple_generator)  # 转换为元组
# print(tuple1)

tuple1 = (100, 200, 300)
print(id(tuple1), tuple1)
tuple1 = tuple1 + (1, 2, 3)
print(id(tuple1), tuple1)

set1 = {1, 2, 3}
set2 = set([1, 2, 3]) # 使用set()函数从列表创建集合
set3 = set()
print(set1, set2, set3)

set1 = {1, 2, 3}
set1.remove(2)
print(set1)