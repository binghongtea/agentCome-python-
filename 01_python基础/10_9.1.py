class Person():
    def __init__(self,name,age):
        self.__name = name

    def printName (self):
        return self.__name

    def __private_method(self):
        print('private_method')

    def do_private_method(self):
        self.__private_method()

    @property
    # 方法转属性
    def eat(self):
        print('eat')

    @property
    # 只读属性
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        if name == '' :
            print('名字不能为空')
        elif name == '李四' :
            print('李四这名字已有')
        else:
            self.__name = name

p = Person('zhangsan',18)
# print(p.__name)
print(p.printName())
print(p._Person__name)

p.do_private_method()
p._Person__private_method()
# p.__private_method()

print(p.name)
# p.name = '111'

p.name = '莉莉丝'
print(p.name)
p.name = ''
p.name = '李四'
print(p.name)