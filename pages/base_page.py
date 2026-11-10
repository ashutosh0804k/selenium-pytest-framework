from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import settings


class BasePage:
    """Shared helpers. Page objects build on these and never call Selenium directly in tests."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.EXPLICIT_WAIT)

    def open(self, path=""):
        self.driver.get(settings.UI_BASE_URL.rstrip("/") + path)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator):
        return self.find(locator).text

    def is_present(self, locator):
        return len(self.find_all(locator)) > 0

    def wait_for_url_contains(self, fragment):
        self.wait.until(EC.url_contains(fragment))
