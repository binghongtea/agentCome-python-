class money:
    def __init__(self, amount):
        self.amount = amount
        self.allowance = amount * 0.5
        self.travel = amount * 0.3
        self.deposit = amount * 0.2

salary = float(input('请输入工资：'))
salary = money(salary)
print('小荷包：', salary.allowance)
print('旅游经费：', salary.travel)
print('存款：', salary.deposit)
