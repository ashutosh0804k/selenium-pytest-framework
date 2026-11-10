import pytest

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_inventory_shows_six_products(inventory):
    assert inventory.item_count() == 6


def test_item_detail_page_matches_listing(inventory, detail_page):
    listed_name = inventory.item_names()[0]
    listed_price = inventory.item_prices()[0]
    inventory.open_first_item()
    assert detail_page.name() == listed_name
    assert detail_page.price() == listed_price


def test_back_to_products_from_detail_page(inventory, detail_page):
    inventory.open_first_item()
    detail_page.back_to_products()
    assert inventory.is_loaded()
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
