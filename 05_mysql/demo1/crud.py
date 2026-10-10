from decimal import Decimal

import uvicorn
from fastapi import FastAPI, Query
from uuid import uuid4

from db import get_connection

app = FastAPI(title="FastAPI 示例")

@app.post('/add_order')
def add_order(
    customer_name: str = Query(..., min_length=1),
    status: str = Query(..., min_length=1),
    amount: Decimal = Query(..., ge=0),
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO orders (order_no, customer_name, status, amount)
                VALUES (%s, %s, %s, %s)
                """,
                (uuid4().hex, customer_name, status, amount),
            )
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return {"msg": "订单新增成功"}

@app.post('/delete_order')
def delete_order(order_id: int = Query(..., ge=1)):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM orders
                WHERE id = %s
                """,
                (order_id,),
            )
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return {"msg": "订单删除成功"}

@app.post('/edit_order')
def edit_order(
    order_id: int = Query(..., ge=1),
    status: str = Query(..., min_length=1),
    amount: Decimal = Query(..., ge=0),
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE orders
                SET status = %s, amount = %s
                WHERE id = %s
                """,
                (status,amount,order_id)
            )
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return {"msg": "订单修改成功"}

@app.post('/select_order')
def select_order(
    customer_name: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id,order_no,customer_name,amount,status,created_at
                FROM orders
                WHERE customer_name LIKE %s
                ORDER BY id DESC
                LIMIT %s OFFSET %s
                """,
                (f"%{customer_name}%", page_size, page_size * (page - 1))
            )
            result = cursor.fetchall()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return result


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
