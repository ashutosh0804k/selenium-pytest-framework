from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ItemDetailPage(BasePage):
    NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    BACK_BUTTON = (By.CSS_SELECTOR, "[data-test='back-to-products']")

    def name(self):
        return self.text_of(self.NAME)

    def price(self):
        return float(self.text_of(self.PRICE).replace("$", ""))

    def back_to_products(self):
        self.click(self.BACK_BUTTON)
        self.wait_for_url_contains("inventory.html")
