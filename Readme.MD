### Kevin Steven Nieto Curaca - A00295466

Lo primero que se debe comprender es el papel que cumple cada elemeto dentro del proyecto.  Dado que estamos usando un patrón POM (Page Object Model) debemos entonces definir una clase que tenga el conjunto de acciones sobre cada página dentro del flujo que vamos a probar, en este caso para poder realizar la compra completa de un producto es necesario añadir la page para el inventory,cart y el checkout, cada unos con su conjunto de métodos que se usana para ejecutar una funcionalidad dentro de la página.

```
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
class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

    def add_product_to_cart(self, product_name):
        
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    
    def go_to_cart(self):
        
        # Presiona el ícono del carrito para ir al carrito de compras
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

         
    def is_inventory_page_displayed(self):
        try:
            # Verificar que el título "Products" está presente en la página
            return self.driver.find_element(By.CLASS_NAME, "title").text == "Products"
        except NoSuchElementException:
            return False    
class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_checkout(self):
        # Encuentra y presiona el botón "Checkout"
        self.driver.find_element(By.ID, "checkout").click()
```
Luego, usando gherkin se establece el escenario y los steps necesarios para ejecutar un test,  siendo ademas de una guía, el susministro de valores para el testing, como el carro a elegir, nombre y demas datos. El escenario en este caso es de la forma:

```
Feature: Checkout de compra

  Scenario: Usuario realiza una compra exitosa
    Given el usuario está en la página de login
    When inicia sesión con "standard_user" y "secret_sauce"
    And agrega el producto "Sauce Labs Backpack" al carrito
    And va al carrito y procede al checkout
    And ingresa su información de compra "Kevin" "Perez" "12345"
    And confirma la compra
    Then el sistema muestra el mensaje "Thank you for your order!"
```
Luego, con los steps del gherkin se define precisamente los steps y lo que se debe realizar usando los POM creados, realizando así el flujo como tal de la aplicación:

```
@given('el usuario está en la página de login')
def step_open_login_page(context):
    context.driver.get("https://www.saucedemo.com/")
    context.login_page = LoginPage(context.driver)

@when('inicia sesión con "{username}" y "{password}"')
def step_login(context, username, password):
    context.login_page.login(username, password)

@when('agrega el producto "{product_name}" al carrito')
def step_add_product(context, product_name):
    context.inventory_page = InventoryPage(context.driver)
    context.inventory_page.add_product_to_cart(product_name)
    #context.inventory_page.go_to_cart()

@when('va al carrito y procede al checkout')
def step_go_to_checkout(context):
    context.cart_page = CartPage(context.driver)
    context.cart_page.go_to_checkout()

@when('ingresa su información de compra "{first_name}" "{last_name}" "{postal_code}"')
def step_enter_checkout_info(context, first_name, last_name, postal_code):
    context.checkout_page = CheckoutPage(context.driver)
    context.checkout_page.enter_checkout_information(first_name, last_name, postal_code)

@when('confirma la compra')
def step_confirm_purchase(context):
    context.checkout_page.finish_checkout()

@then('el sistema muestra el mensaje "{message}"')
def step_verify_success_message(context, message):
    assert context.checkout_page.get_success_message() == message
    context.driver.quit()
```
Ya con el  testing defindio no queda más que correr el test con el comando `behave`. 

Es importante aclarar que el driver debe provenir del contexto para poder aplicar todas las reglas, como el bloqueo de los popups que se configuran en las optinos del driver.

```
    # Configuración para evitar popups y advertencias de seguridad
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--password-store=basic")
    options.add_argument("--headless")  # Modo sin interfaz gráfica (importante en GitHub Actions)
    options.add_argument("--no-sandbox")  # Necesario en contenedores como GitHub Actions
    options.add_argument("--disable-dev-shm-usage")  # Evita problemas en entornos virtualizados
    options.add_argument("--disable-gpu")  # Solo en caso de necesitar compatibilidad con GPU

    options.add_argument("--disable-features=PasswordProtectionService")
    options.add_argument("--disable-features=PasswordLeakDetection")
    
    user_data_dir = os.path.join(tempfile.gettempdir(), 'chrome_profile')
    options.add_argument(f"--user-data-dir={user_data_dir}")

    # Preferencias experimentales para desactivar advertencias
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "profile.default_content_setting_values.notifications": 2,
        "safebrowsing.enabled": False,
        "safebrowsing.disable_download_protection": True,
        "credentials_enable_autosignin": False
    })
```
Es necesario usar la linea
```
service = Service(ChromeDriverManager().install())  

```
Para que cuando el agente esté ejecutando el test pueda el mismo instalar un driver para poder interactuar con la pagina a testear.
