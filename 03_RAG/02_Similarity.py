import numpy as np

vector1 = np.array([1,2,3])
vector2 = np.array([4,5,6])
vector3 = np.array([7,8,9])
print(vector1)
print(vector2)

# 点积 （简化版余弦相似度
print(np.dot(vector1, vector2))
print(np.dot(vector1, vector3))