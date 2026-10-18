import os
from contextlib import closing

import psycopg2


def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"], connect_timeout=3)


def add_product(name: str, price: float) -> dict:
    with closing(get_connection()) as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO products (name, price) VALUES (%s, %s) "
                    "RETURNING id, name, price",
                    (name, price),
                )
                row = cursor.fetchone()
    return {"id": row[0], "name": row[1], "price": float(row[2])}


def find_product(product_id: int) -> dict | None:
    with closing(get_connection()) as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, price FROM products WHERE id = %s",
                    (product_id,),
                )
                row = cursor.fetchone()
    if row is None:
        return None
    return {"id": row[0], "name": row[1], "price": float(row[2])}


def get_products() -> list[dict]:
    with closing(get_connection()) as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, price FROM products ORDER BY id")
                rows = cursor.fetchall()
    return [
        {"id": row[0], "name": row[1], "price": float(row[2])}
        for row in rows
    ]
