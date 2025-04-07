import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Call this function after navigating to pages that might trigger the popup
class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

    def add_product_to_cart(self, product_name):
        
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    
    def go_to_cart(self):
        
        # Presiona el ícono del carrito para ir al carrito de compras
        self.driver.find_element(By.ID, "shopping_cart_container").click()

         
    def is_inventory_page_displayed(self):
        try:
            # Verificar que el título "Products" está presente en la página
            return self.driver.find_element(By.CLASS_NAME, "title").text == "Products"
        except NoSuchElementException:
            return False    
