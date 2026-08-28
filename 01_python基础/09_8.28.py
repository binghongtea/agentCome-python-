class Person:
    '''人类'''
    home = '地球'
    def __init__(self,name,age,food):
        self.age = 0
        self.name = name
        self.food = food
    def eat(self):
        print(f'eating {self.food}')
    def drink(self,water):
        self.water = water
        print(f'drinking {self.water}')

home = Person.home
eat = Person.eat
drink = Person.drink
print(home)
print(eat)
print(drink)
print(Person.__doc__)

class Man(Person):
    '''男人'''
    sex = 'man'

zhangsan = Man('zhangsan',18,'tomato')
print(zhangsan)
print(zhangsan.__doc__)
print(zhangsan.sex)
zhangsan.eat()
zhangsan.drink('可口可乐')
