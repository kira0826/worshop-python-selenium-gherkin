from selenium.webdriver.common.by import By

class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_checkout(self):
        # Encuentra y presiona el botón "Checkout"
        self.driver.find_element(By.ID, "checkout").click()
