from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    def enter_checkout_information(self, first_name, last_name, postal_code):
        self.driver.find_element(By.ID, "first-name").send_keys(first_name)
        self.driver.find_element(By.ID, "last-name").send_keys(last_name)
        self.driver.find_element(By.ID, "postal-code").send_keys(postal_code)
        self.driver.find_element(By.ID, "continue").click()

    def finish_checkout(self):
        self.driver.find_element(By.ID, "finish").click()

    def get_success_message(self):
        return self.driver.find_element(By.CLASS_NAME, "complete-header").text
