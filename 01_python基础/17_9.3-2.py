import copy

list1 = [1,2,3,[1,2,3]]

list2 = copy.copy(list1)
print(list1)
print(list2)

list1[0] = 2
list1[3].append(5)

print(list1)
print(list2)