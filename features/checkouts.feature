Feature: Checkout de compra

  Scenario: Usuario realiza una compra exitosa
    Given el usuario está en la página de login
    When inicia sesión con "standard_user" y "secret_sauce"
    And agrega el producto "Sauce Labs Backpack" al carrito
    And va al carrito y procede al checkout
    And ingresa su información de compra "Kevin" "Perez" "12345"
    And confirma la compra
    Then el sistema muestra el mensaje "Thank you for your order!"
