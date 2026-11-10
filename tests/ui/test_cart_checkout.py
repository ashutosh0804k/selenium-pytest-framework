import pytest

pytestmark = pytest.mark.ui


def test_cart_badge_counts_added_items(inventory):
    inventory.add_first_n(3)
    assert inventory.cart_count() == 3


def test_remove_item_updates_badge(inventory):
    inventory.add_first_n(2)
    inventory.remove_first_item()
    assert inventory.cart_count() == 1


def test_added_item_appears_in_cart(inventory, cart_page):
    first_name = inventory.item_names()[0]
    inventory.add_item_by_index(0)
    inventory.open_cart()
    assert cart_page.item_names() == [first_name]


def test_remove_item_from_cart_page(inventory, cart_page):
    inventory.add_first_n(2)
    inventory.open_cart()
    cart_page.remove_first_item()
    assert cart_page.item_count() == 1


def test_continue_shopping_returns_to_inventory(inventory, cart_page):
    inventory.add_item_by_index(0)
    inventory.open_cart()
    cart_page.continue_shopping()
    assert inventory.is_loaded()
    assert inventory.cart_count() == 1


def test_checkout_subtotal_matches_item_prices(inventory, cart_page, checkout_page):
    prices = inventory.item_prices()
    inventory.add_first_n(2)
    # the add buttons keep their page order, so the first two items are in the cart
    expected = round(prices[0] + prices[1], 2)
    inventory.open_cart()
    cart_page.checkout()
    checkout_page.fill_info("Ashutosh", "Khatavkar", "13210")
    assert checkout_page.subtotal() == expected


def test_cancel_checkout_returns_to_cart(inventory, cart_page, checkout_page):
    inventory.add_item_by_index(0)
    inventory.open_cart()
    cart_page.checkout()
    checkout_page.cancel()
    assert cart_page.item_count() == 1


@pytest.mark.smoke
def test_full_checkout_flow(inventory, cart_page, checkout_page):
    inventory.add_item_by_index(0)
    inventory.open_cart()
    cart_page.checkout()
    checkout_page.fill_info("Ashutosh", "Khatavkar", "13210")
    checkout_page.finish()
    assert checkout_page.confirmation() == "Thank you for your order!"


@pytest.mark.parametrize(
    "first,last,postal,expected",
    [
        ("", "Khatavkar", "13210", "First Name is required"),
        ("Ashutosh", "", "13210", "Last Name is required"),
        ("Ashutosh", "Khatavkar", "", "Postal Code is required"),
    ],
)
def test_checkout_requires_all_fields(
    inventory, cart_page, checkout_page, first, last, postal, expected
):
    inventory.add_item_by_index(0)
    inventory.open_cart()
    cart_page.checkout()
    checkout_page.fill_info(first, last, postal)
    assert expected in checkout_page.error_message()
