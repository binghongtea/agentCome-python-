# 假设我们用一个常见的 Embedding 模型 (如 OpenAI 或 HuggingFace)
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# 我们的数据
texts = ["我想买个手机", "苹果新款多少钱", "今天天气不错"]

# 变成向量 (Embeddings)
vectors = model.encode(texts)

print(f"这句话：'{texts[0]}'")
# 打印前5个数字看看，其实后面还有几百个，代表它的精确坐标
print(f"变成了坐标：{vectors[0][:5]} ...") 

# 结果示意：
# 这句话：'我想买个手机'
# 变成了坐标：[-0.023, 0.542, -0.112, 0.004, 0.887] ...