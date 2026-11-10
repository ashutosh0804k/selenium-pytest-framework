from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEMS = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='remove']")

    def item_names(self):
        return [e.text for e in self.find_all(self.ITEM_NAMES)]

    def item_count(self):
        return len(self.find_all(self.ITEMS))

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def remove_first_item(self):
        self.find_all(self.REMOVE_BUTTONS)[0].click()

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING)
        self.wait_for_url_contains("inventory.html")
