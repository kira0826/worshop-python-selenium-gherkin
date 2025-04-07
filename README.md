### Kevin Steven Nieto Curaca - A00295466

The first thing to understand is the role each component plays within the project. Since we are using the **Page Object Model (POM)** design pattern, we need to define a class that contains the set of actions for each page involved in the test flow. 

To successfully complete a purchase, we must include page objects for **Inventory**, **Cart**, and **Checkout**, each one encapsulating the methods required to interact with its respective page.

```python
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
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    def is_inventory_page_displayed(self):
        try:
            return self.driver.find_element(By.CLASS_NAME, "title").text == "Products"
        except NoSuchElementException:
            return False    

class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def go_to_checkout(self):
        self.driver.find_element(By.ID, "checkout").click()
```

---

Next, using **Gherkin**, we define the scenario and steps required to run the test. Gherkin not only acts as a guide but also provides test data such as the selected product, user name, and other details. Here's the scenario:

```gherkin
Feature: Purchase Checkout

  Scenario: User successfully completes a purchase
    Given the user is on the login page
    When they log in with "standard_user" and "secret_sauce"
    And they add the product "Sauce Labs Backpack" to the cart
    And they go to the cart and proceed to checkout
    And they enter their purchase information "Kevin" "Perez" "12345"
    And they confirm the purchase
    Then the system displays the message "Thank you for your order!"
```

Using these Gherkin steps, we then define the corresponding step definitions that interact with the POM classes to simulate the actual application flow:

```python
@given('the user is on the login page')
def step_open_login_page(context):
    context.driver.get("https://www.saucedemo.com/")
    context.login_page = LoginPage(context.driver)

@when('they log in with "{username}" and "{password}"')
def step_login(context, username, password):
    context.login_page.login(username, password)

@when('they add the product "{product_name}" to the cart')
def step_add_product(context, product_name):
    context.inventory_page = InventoryPage(context.driver)
    context.inventory_page.add_product_to_cart(product_name)

@when('they go to the cart and proceed to checkout')
def step_go_to_checkout(context):
    context.cart_page = CartPage(context.driver)
    context.cart_page.go_to_checkout()

@when('they enter their purchase information "{first_name}" "{last_name}" "{postal_code}"')
def step_enter_checkout_info(context, first_name, last_name, postal_code):
    context.checkout_page = CheckoutPage(context.driver)
    context.checkout_page.enter_checkout_information(first_name, last_name, postal_code)

@when('they confirm the purchase')
def step_confirm_purchase(context):
    context.checkout_page.finish_checkout()

@then('the system displays the message "{message}"')
def step_verify_success_message(context, message):
    assert context.checkout_page.get_success_message() == message
    context.driver.quit()
```

Once the test is defined, it can be executed using the command `behave`.

It's important to note that the **WebDriver instance must be passed through the context** to properly apply configurations such as blocking popups or handling browser options.

```python
# Configuration to suppress popups and security warnings
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--password-store=basic")
options.add_argument("--headless")  # Useful for GitHub Actions
options.add_argument("--no-sandbox")  # Required in container environments
options.add_argument("--disable-dev-shm-usage")  # Avoids shared memory issues
options.add_argument("--disable-gpu")  # GPU compatibility

options.add_argument("--disable-features=PasswordProtectionService")
options.add_argument("--disable-features=PasswordLeakDetection")

user_data_dir = os.path.join(tempfile.gettempdir(), 'chrome_profile')
options.add_argument(f"--user-data-dir={user_data_dir}")

# Experimental options to suppress additional warnings
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

Additionally, this line is required:

```python
service = Service(ChromeDriverManager().install())
```

This ensures that when the pipeline agent runs the test, it can automatically install the appropriate ChromeDriver to interact with the webpage.

---
GitHub Actions Pipeline

The following GitHub Actions pipeline runs the test suite whenever a pull request is made to the `main` branch. It ensures everything is executed in a Python virtual environment, with the required packages installed including `selenium`, `behave`, and `webdriver-manager`.

It also uses `behave --format json --out reports/report.json` to generate a test report, which is uploaded as an artifact using `actions/upload-artifact@v4`. This artifact is stored as a **blob** (Binary Large Object) in GitHub.

```yaml
name: Run Selenium Tests with Behave

on:
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install Dependencies
        run: |
          python -m venv venv   
          source venv/bin/activate
          pip install --upgrade pip
          pip install selenium behave
          pip install webdriver-manager

      - name: Run Behave Tests
        run: |
          source venv/bin/activate
          mkdir -p reports
          behave --format json --out reports/report.json  
      
      - name: Upload Test Reports
        uses: actions/upload-artifact@v4
        with:
          name: test-reports
          path: reports/
```
