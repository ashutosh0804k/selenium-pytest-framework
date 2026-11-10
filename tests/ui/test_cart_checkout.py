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
