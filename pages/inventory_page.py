import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

    def add_product_to_cart(self, product_name):
        # Cierra el popup si aparece
        self.close_password_popup()
        # Encuentra el producto por su nombre y presiona "Add to cart"
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        time.sleep(4)

    def go_to_cart(self):
        # Cierra el popup si aparece
        self.close_password_popup()
        # Presiona el ícono del carrito para ir al carrito de compras
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    def close_password_popup(self):
        """ Intenta cerrar el popup de cambio de contraseña si aparece. """
        try:
            popup_button = self.driver.find_element(By.XPATH, "//button[text()='OK']")
            popup_button.click()
            print("✅ Popup de contraseña cerrado.")
        except NoSuchElementException:
            print("ℹ️ No se encontró el popup de contraseña.")
