from contextlib import closing

from fastapi.testclient import TestClient

from app.database import get_connection
from app.main import app

client = TestClient(app)


def test_database_connection():
    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            assert cursor.fetchone()[0] == 1


def test_health_route():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_product_is_stored_in_postgres():
    response = client.post("/products", json={"name": "Keyboard", "price": 1500})
    assert response.status_code == 201
    product = response.json()
    assert product == {"id": 1, "name": "Keyboard", "price": 1500.0}

    with closing(get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, price FROM products WHERE id = %s", (1,))
            row = cursor.fetchone()
    assert row[0] == "Keyboard"
    assert float(row[1]) == 1500.0


def test_get_existing_product_from_postgres():
    with closing(get_connection()) as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO products (name, price) VALUES (%s, %s)",
                    ("Mouse", 550),
                )
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Mouse", "price": 550.0}


def test_get_missing_product():
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_list_products_reads_postgres():
    with closing(get_connection()) as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO products (name, price) VALUES (%s, %s), (%s, %s)",
                    ("Pen", 25, "Notebook", 100),
                )
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Pen", "price": 25.0},
        {"id": 2, "name": "Notebook", "price": 100.0},
    ]


def test_invalid_product_returns_validation_error():
    response = client.post("/products", json={"name": "Bad", "price": -1})
    assert response.status_code == 422
