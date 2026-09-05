# import os
#
# for element in [1, 2, 3]:
#     print(element)
# for element in (1, 2, 3):
#     print(element)
# for key in {"one": 1, "two": 2}:
#     print(key)
# for char in "123":
#     print(char)
#
# with open("myfile.txt", "w") as f:
#     f.write("H\ne\nl\nl\no\n \nW\no\nr\nl\nd\n")
# for line in open("myfile.txt"):
#     print(line, end="")
# os.remove("myfile.txt")

# list = [1,2,3]
# it = iter(list)
# # print(next(it))
# # print(next(it))
# # print(next(it))
# # print(next(it))
# for i in it:
#     print(i)

# class Reverse:
#     '''反向迭代器'''
#     def __init__(self,data):
#         self.data = data
#         self.index = len(data)
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         if self.index == 0:
#             raise StopIteration
#         self.index -= 1
#         return self.data[self.index]
#
# list1 = Reverse([2,3,2,44,55])
# print(list(Reverse('hello')))
# for item in list1:
#     print(item)

# generator = (x for x in range(10))
# print(generator)
# for x in generator:
#     print(x)

# def fibo(n):
#     a,b,counter = 0,1,1
#     while counter <= n:
#         yield counter
#         counter = a+b
#         a,b = b,a+b
#     else:
#         return "done"

# f = fibo(10)
# try:
#     while True:
#         print(next(f))
# except StopIteration as e:
#     print(e.value)

def linear(a, b):
  def inner(x):
    return a * x + b

  return inner

y1 = linear(1, 2)
objects = y1.__closure__
print(objects)
print(objects[0].cell_contents) # 1
print(objects[1].cell_contents) # 2