import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
def before_scenario(context, scenario):
    """
    Esta función se ejecuta antes de cada escenario de prueba.
    Inicializa el WebDriver y lo almacena en el contexto.
    """
    options = Options()

    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_argument("--password-store=basic")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_enabled": False,  
        "profile.default_content_setting_values.notifications": 2,  # Bloquea notificaciones emergentes
        "profile.password_manager_leak_detection.enabled": False,  # ❌ Desactiva advertencias de contraseñas comprometidas
        "safebrowsing.enabled": False  # Disable Safe Browsing (this prevents the popup)
    })
    
    prefs = {"credentials_enable_service": False,
         "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)

    service = Service("/usr/bin/chromedriver")  # Ruta específica de ChromeDriver
    context.driver = webdriver.Chrome(service=service, options=options)
    context.driver.implicitly_wait(15)
    context.driver.maximize_window()
    
    try:
        context.driver.switch_to.alert.dismiss()
    except:
        pass 

def after_step(context, step):
    time.sleep(0.5)

def after_scenario(context, scenario):
    """
    Esta función se ejecuta después de cada escenario de prueba.
    Cierra el navegador para limpiar después de cada prueba.
    """
    context.driver.quit()


    