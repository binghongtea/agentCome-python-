class Person:
    '''人类'''
    home = 'earth'
    def __init__(self,name):
        self.name = name

    def eat(self):
        print('eating')

class YellowPerson(Person):
    color = 'yellow'
    def __init__(self,space,**kwargs):
        self.space = space

class Student(Person):
    '''学生'''
    def __init__(self,name,grade,**kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.grade = grade

class ChineseStudent(Student,YellowPerson):
    '''中国学生'''
    country = 'China'
    def __init__(self,name,grade,space):
        super().__init__(name=name,grade=grade,space=space)


    def study(self):
        print('先吃再学')
        super().eat()
        Person.eat(self)
        print('study')

y = ChineseStudent('张三','九年级','浙江')
y.eat()
print('name:', y.name)
print('grade:', y.grade)
print('country:', y.country)
print('color:', y.color)
print('space:', y.space)
y.study()