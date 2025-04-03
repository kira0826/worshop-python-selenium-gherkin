from behave import given, when, then
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from selenium import webdriver

@given('el usuario está en la página de login')
def step_open_login_page(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://www.saucedemo.com/")
    context.login_page = LoginPage(context.driver)

@when('inicia sesión con "{username}" y "{password}"')
def step_login(context, username, password):
    context.login_page.login(username, password)

@when('agrega el producto "{product_name}" al carrito')
def step_add_product(context, product_name):
    context.inventory_page = InventoryPage(context.driver)
    context.inventory_page.add_product_to_cart(product_name)
    context.inventory_page.go_to_cart()

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
