import pytest

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_inventory_shows_six_products(inventory):
    assert inventory.item_count() == 6


def test_sort_name_a_to_z(inventory):
    inventory.sort_by("az")
    names = inventory.item_names()
    assert names == sorted(names)


def test_sort_name_z_to_a(inventory):
    inventory.sort_by("za")
    names = inventory.item_names()
    assert names == sorted(names, reverse=True)


def test_sort_price_low_to_high(inventory):
    inventory.sort_by("lohi")
    prices = inventory.item_prices()
    assert prices == sorted(prices)


def test_sort_price_high_to_low(inventory):
    inventory.sort_by("hilo")
    prices = inventory.item_prices()
    assert prices == sorted(prices, reverse=True)
