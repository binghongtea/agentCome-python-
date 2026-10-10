from decimal import Decimal
from uuid import uuid4

from db import get_connection


def main():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            # 1. 新增订单
            order_no = uuid4().hex

            cursor.execute(
                """
                INSERT INTO orders
                    (order_no, customer_name, amount)
                VALUES (%s, %s, %s)
                """,
                (order_no, "张三", Decimal("99.90")),
            )

            order_id = cursor.lastrowid
            print("新增订单 ID：", order_id)

            # 2. 根据 ID 查询一条订单
            cursor.execute(
                """
                SELECT id, order_no, customer_name, amount, status
                FROM orders
                WHERE id = %s
                """,
                (order_id,),
            )

            order = cursor.fetchone()
            print("查到订单：", order)

            if order is not None:
                print("订单金额：", order["amount"])

            # 3. 修改订单状态
            cursor.execute(
                """
                UPDATE orders
                SET status = %s
                WHERE id = %s AND status = %s
                """,
                ("cancelled", order_id, "pending"),
            )

            print("修改行数：", cursor.rowcount)

            # 4. 查询客户最近的订单
            cursor.execute(
                """
                SELECT id, customer_name, amount, status
                FROM orders
                WHERE customer_name = %s
                ORDER BY id DESC
                LIMIT %s
                """,
                ("张三", 10),
            )

            for item in cursor.fetchall():
                print("列表中的订单：", item)

            # 5. 删除刚才创建并取消的练习订单
            cursor.execute(
                """
                DELETE FROM orders
                WHERE id = %s AND status = %s
                """,
                (order_id, "cancelled"),
            )

            print("删除行数：", cursor.rowcount)

        # 本例把以上修改作为一组操作提交
        conn.commit()
        print("提交成功")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

def update_order_paid(order_id: int):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE orders
                SET status = %s
                WHERE id = %s AND status = %s
                """,
                ("paid", order_id, "pending")
            )

            if cursor.rowcount != 1:
                raise Exception("订单状态更新失败")

            cursor.execute(
                """
                INSERT INTO order_logs
                    (order_id,action)
                    VALUES (%s, %s)
                """,
                (order_id, "mark_paid")
            )

            conn.commit()

    except Exception:
        conn.rollback()
        raise
    

    finally:
        conn.close()

if __name__ == "__main__":
    # main()
    update_order_paid(4)