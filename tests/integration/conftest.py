import os
from contextlib import closing

import psycopg2
import pytest


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        pytest.fail("DATABASE_URL is not set: PostgreSQL is required for integration tests")
    with closing(psycopg2.connect(db_url)) as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS products (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        price NUMERIC(10, 2) NOT NULL CHECK (price >= 0)
                    )
                    """
                )


@pytest.fixture(autouse=True)
def clean_database(prepare_database):
    db_url = os.environ["DATABASE_URL"]
    with closing(psycopg2.connect(db_url)) as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE products RESTART IDENTITY")
    yield
    with closing(psycopg2.connect(db_url)) as connection:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE products RESTART IDENTITY")
