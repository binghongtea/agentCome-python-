# from my_add import *
import my_add as a1

class book:

    color = 'blue'
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def look(self):
        print('看书')

b1 = book('语文',19)

print(a1.add(1,2))
print(a1.num)
print(a1.num1)

import sys
print(sys.path)

sys.path.append('dd/..')

print(sys.path)

print(dir(a1))
print(dir(b1))
