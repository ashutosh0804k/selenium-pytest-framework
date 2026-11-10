from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")

    CANCEL_BUTTON = (By.ID, "cancel")
    SUBTOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")

    def cancel(self):
        self.click(self.CANCEL_BUTTON)
        self.wait_for_url_contains("cart")

    def subtotal(self):
        """Parses 'Item total: $39.98' into 39.98"""
        return float(self.text_of(self.SUBTOTAL).split("$")[1])

    def fill_info(self, first, last, postal):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)
        self.click(self.CONTINUE_BUTTON)

    def finish(self):
        self.click(self.FINISH_BUTTON)

    def error_message(self):
        return self.text_of(self.ERROR)

    def confirmation(self):
        return self.text_of(self.COMPLETE_HEADER)
