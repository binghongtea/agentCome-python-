a = [1,2,3]
b = a

print(b is a)
print(b == a)

b = a[:]
print(b)
print(b is a)
print(b == a)