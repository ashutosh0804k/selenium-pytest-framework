import pytest

from config import settings
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.item_detail_page import ItemDetailPage
from pages.login_page import LoginPage


@pytest.fixture
def login_page(driver):
    return LoginPage(driver).load()


@pytest.fixture
def inventory(driver, login_page):
    """A logged-in standard user sitting on the inventory page."""
    login_page.login(settings.STANDARD_USER, settings.VALID_PASSWORD)
    page = InventoryPage(driver)
    assert page.is_loaded()
    return page


@pytest.fixture
def detail_page(driver):
    return ItemDetailPage(driver)


@pytest.fixture
def cart_page(driver):
    return CartPage(driver)


@pytest.fixture
def checkout_page(driver):
    return CheckoutPage(driver)
