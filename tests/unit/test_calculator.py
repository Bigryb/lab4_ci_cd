import pytest

from app.calculator import apply_discount, calculate_total


def test_total_normal():
    assert calculate_total(19.99, 3) == 59.97


def test_total_zero_price():
    assert calculate_total(0, 5) == 0


def test_total_negative_price():
    with pytest.raises(ValueError):
        calculate_total(-10, 2)


def test_total_zero_quantity():
    with pytest.raises(ValueError):
        calculate_total(10, 0)

def test_total_negative_quantity():
    with pytest.raises(ValueError):
        calculate_total(10, -1)

def test_discount_normal():
    assert apply_discount(100, 10) == 90


def test_discount_zero():
    assert apply_discount(100, 0) == 100

def test_discount_full():
    assert apply_discount(100, 100) == 0

def test_discount_negative():
    with pytest.raises(ValueError):
        apply_discount(100, -5)


def test_discount_above_100():
    with pytest.raises(ValueError):
        apply_discount(100, 120)
