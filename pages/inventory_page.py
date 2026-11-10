from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    ADD_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='remove']")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def is_loaded(self):
        self.wait_for_url_contains("inventory")
        return self.text_of(self.TITLE) == "Products"

    def item_count(self):
        return len(self.find_all(self.ITEMS))

    def item_names(self):
        return [e.text for e in self.find_all(self.ITEM_NAMES)]

    def item_prices(self):
        return [float(e.text.replace("$", "")) for e in self.find_all(self.ITEM_PRICES)]

    def add_item_by_index(self, index=0):
        self.find_all(self.ADD_BUTTONS)[index].click()

    def add_first_n(self, n):
        for _ in range(n):
            # the first "add" button disappears once clicked, so always take index 0
            self.add_item_by_index(0)

    def remove_first_item(self):
        self.find_all(self.REMOVE_BUTTONS)[0].click()

    def cart_count(self):
        if not self.is_present(self.CART_BADGE):
            return 0
        return int(self.text_of(self.CART_BADGE))

    def sort_by(self, value):
        """value is one of: az, za, lohi, hilo"""
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(value)

    def open_cart(self):
        self.click(self.CART_LINK)
        self.wait_for_url_contains("cart")

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
