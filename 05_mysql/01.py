import pymysql
from pymysql.cursors import DictCursor


# 建立连接
conn = pymysql.connect(
    host="localhost",       # 数据库地址
    port=3306,              # 数据库端口
    user="root",
    password="yangzekai12",     # 本地练习用，正式项目放到环境变量中
    database="demo",
    charset="utf8mb4",
    cursorclass=DictCursor, # 查询结果返回字典
    autocommit=False,
)


# 新增：返回新增用户的 ID
def create_user(name, age):
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (name, age) VALUES (%s, %s)",
            (name, age),
        )
        return cursor.lastrowid


# 查询单个用户：不存在时返回 None
def get_user(user_id):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT id, name, age FROM users WHERE id = %s",
            (user_id,),
        )
        return cursor.fetchone()


# 查询用户列表
def list_users():
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, age FROM users ORDER BY id")
        return cursor.fetchall()


# 修改：返回实际修改的行数
def update_user(user_id, name, age):
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE users SET name = %s, age = %s WHERE id = %s",
            (name, age, user_id),
        )
        return cursor.rowcount


# 删除：返回删除的行数
def delete_user(user_id):
    with conn.cursor() as cursor:
        cursor.execute(
            "DELETE FROM users WHERE id = %s",
            (user_id,),
        )
        return cursor.rowcount


# 调用示例
try:
    user_id = create_user("张三", 20)
    print("新增用户 ID：", user_id)

    print("查询用户：", get_user(user_id))
    # 例如：{'id': 1, 'name': '张三', 'age': 20}

    update_user(user_id, "张三", 21)
    print("修改后：", get_user(user_id))

    print("用户列表：", list_users())

    # deleted = delete_user(user_id)
    # print("删除行数：", deleted)

    # 上面的写入操作统一提交
    conn.commit()

except Exception:
    # 出错时，撤销本次尚未提交的修改
    conn.rollback()
    raise

finally:
    conn.close()