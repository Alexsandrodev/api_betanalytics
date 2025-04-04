from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import logging
from time import sleep

# Configurações globais
CHROME_OPTIONS = {
    'binary_location': '/usr/bin/google-chrome',
    'args': [
        '--no-sandbox',
        '--disable-gpu',
        '--disable-dev-shm-usage',
        '--disable-images',
        '--disable-javascript',
        '--window-size=1920,1080',
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    ],
    'exclude_switches': ['enable-automation', 'enable-logging'],
    'prefs': {
        'intl.accept_languages': 'pt-BR',
        'timezone.override': 'America/Sao_Paulo'
    }
}

CAMPEONATOS = {
    "copaAmerica": "Copa America",
    "tacaGloriaEterna": "Taça Glória eterna",
    "euro": "Euro",
    "britishDerbies": "British Derbies",
    "ligaEspanhola": "Liga Espanhola",
    "scudettoItaliano": "Scudetto Italiano",
    "campeonatoItaliano": "Campeonato Italiano",
    "copaDasEstrelas": "Copa das estrelas"
}

def data_atualizacao():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def format_name(campeonato):
    return CAMPEONATOS.get(campeonato, campeonato)

def setup_driver():
    options = Options()
    for arg in CHROME_OPTIONS['args']:
        options.add_argument(arg)
    options.set_capability("browserName", "chrome")
    options.set_capability("goog:chromeOptions", {
        "args": CHROME_OPTIONS['args'],
        "excludeSwitches": CHROME_OPTIONS['exclude_switches'],
        "prefs": CHROME_OPTIONS['prefs']
    })
    
    driver = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        options=options
    )
    return driver

def click_element(driver, locator, max_attempts=3, timeout=10):
    for _ in range(max_attempts):
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable(locator))
            element.click()
            return True
        except:
            sleep(1)
    return False

def get_html(campeonato):
    driver = None
    try:
        driver = setup_driver()
        url = "https://www.betano.bet.br/virtuals/futebol/"
        liga = format_name(campeonato)
        
        driver.get(url)
        logging.info(f'Acessando {url} para {campeonato}')

        # Elementos para clicar (com fallback silencioso)
        elements_to_click = [
            (By.XPATH, '//button[span[text()="Sim"]]'),  
            (By.CSS_SELECTOR, 'button[type="button"]'),    
            (By.LINK_TEXT, liga),                          
            (By.CSS_SELECTOR, "div[data-qa='virtuals-results-toggle-button']") 
        ]

        for locator in elements_to_click:
            if not click_element(driver, locator):
                logging.warning(f"Elemento não clicável: {locator}")

        # Esperar resultados carregarem
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
            ".tw-flex.tw-items-center.tw-justify-center.tw-mt-m.tw-mb-n.tw-mx-n")))
        
        return driver.page_source

    except Exception as e:
        logging.error(f"Erro no scraping de {campeonato}: {str(e)}")
        raise e
    finally:
        if driver:
            driver.quit()