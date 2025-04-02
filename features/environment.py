import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def before_scenario(context, scenario):
    """
    Esta función se ejecuta antes de cada escenario de prueba.
    Inicializa el WebDriver y lo almacena en el contexto.
    """
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })
    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(15)
    context.driver.maximize_window()

def after_step(context, step):
    time.sleep(0.5)

def after_scenario(context, scenario):
    """
    Esta función se ejecuta después de cada escenario de prueba.
    Cierra el navegador para limpiar después de cada prueba.
    """
    context.driver.quit()


    