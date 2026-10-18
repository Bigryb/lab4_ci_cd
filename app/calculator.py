def calculate_total(price: float, quantity: int) -> float:
    if price < 0:
        raise ValueError("Price cannot be negative")
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    return round(price * quantity, 2)


def apply_discount(total: float, discount_percent: float) -> float:
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    return round(total * (1 - discount_percent / 100), 2)
