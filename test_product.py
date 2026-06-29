import pytest
from products import Product


def test_create_normal_product():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active()


def test_create_invalid_product():
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_becomes_inactive_at_zero_quantity():
    product = Product("MacBook Air M2", price=1450, quantity=10)
    product.buy(10)
    assert product.quantity == 0
    assert not product.is_active()


def test_buy_modifies_quantity_and_returns_price():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    total = product.buy(2)
    assert total == 2900
    assert product.quantity == 98


def test_buy_more_than_available_raises():
    product = Product("MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError):
        product.buy(10)
