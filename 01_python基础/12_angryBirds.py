class Bird():
    '''鸟'''
    def __init__(self, name, color,skill_description):
        self.name = name
        self.color = color
        self.skill_description = skill_description

class RedBird(Bird):
    '''红鸟'''
    def __init__(self, name, color,skill_description,damage):
        super().__init__(name,color,skill_description)
        self.damage = damage

    def fly(self):
        print('稳定速度飞行')


class YellowBird(Bird):
    '''黄鸟'''
    def __init__(self, name, color,skill_description,damage):
        super().__init__(name,color,skill_description)
        self.damage = damage

    def fly(self):
        print('快速飞行')

class Obstacle():
    '''障碍物'''
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength

    def be_attacked(self,bird):
        if isinstance(bird,RedBird):
            damage = bird.damage
        elif isinstance(bird,YellowBird):
            damage = bird.damage
        self.strength -= damage
        if self.strength <= 0:
            print(f'{self.name}被摧毁了')
        else:
            print(f'{self.name}还有{self.strength}点血')

red_bird = RedBird('redBird','red','稳定速度飞行',80)
red_bird.fly()
yellow_bird = YellowBird('yellowBird','yellow','快速飞行',60)
yellow_bird.fly()

ob1 = Obstacle('木头',100)
ob2 = Obstacle('铁块',200)

ob1.be_attacked(red_bird)
ob1.be_attacked(yellow_bird)
ob2.be_attacked(red_bird)
ob2.be_attacked(yellow_bird)
ob2.be_attacked(red_bird)