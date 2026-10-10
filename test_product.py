"""Unit tests for the product classes and promotions."""
import pytest
from products import Product, NonStockedProduct, LimitedProduct
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount
from store import Store


def test_create_normal_product() -> None:
    """Test that a normal product is created with the right values."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active()


def test_create_invalid_product() -> None:
    """Test that invalid details raise a ValueError."""
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_product_becomes_inactive_at_zero_quantity() -> None:
    """Test that a product becomes inactive at quantity 0."""
    product = Product("MacBook Air M2", price=1450, quantity=10)
    product.buy(10)
    assert product.quantity == 0
    assert not product.is_active()


def test_buy_modifies_quantity_and_returns_price() -> None:
    """Test that buying changes the quantity and returns the right price."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    total = product.buy(2)
    assert total == 2900
    assert product.quantity == 98


def test_buy_more_than_available_raises() -> None:
    """Test that buying more than in stock raises a ValueError."""
    product = Product("MacBook Air M2", price=1450, quantity=5)
    with pytest.raises(ValueError):
        product.buy(10)


def test_non_stocked_product_keeps_quantity() -> None:
    """Test that a non stocked product keeps its quantity."""
    windows = NonStockedProduct("Windows License", price=125)
    assert windows.buy(3) == 375
    assert windows.quantity == 0
    assert windows.is_active()


def test_limited_product_over_maximum_raises() -> None:
    """Test that buying more than the maximum raises a ValueError."""
    shipping = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    with pytest.raises(ValueError):
        shipping.buy(2)
    assert shipping.buy(1) == 10


def test_promotions_change_the_price() -> None:
    """Test that every promotion returns the right price."""
    product = Product("Google Pixel 7", price=100, quantity=100)
    product.set_promotion(SecondHalfPrice("Second Half price!"))
    assert product.buy(2) == 150
    product.set_promotion(ThirdOneFree("Third One Free!"))
    assert product.buy(3) == 200
    product.set_promotion(PercentDiscount("30% off!", percent=30))
    assert product.buy(1) == 70


def test_store_counts_only_active_products() -> None:
    """Test that the store total ignores inactive products."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    pixel.deactivate()
    best_buy = Store([mac, pixel])
    assert best_buy.get_total_quantity() == 100
    assert best_buy.get_all_products() == [mac]
