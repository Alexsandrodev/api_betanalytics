from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def data_atualizacao():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def format_name(nome):
    nomes = {
        "copaAmerica": "Copa America",
        "tacaGloriaEterna": "Taça Glória eterna",
        "euro": "Euro",
        "britishDerbies": "British Derbies",
        "ligaEspanhola": "Liga Espanhola",
        "scudettoItaliano": "Scudetto Italiano",
        "campeonatoItaliano": "Campeonato Italiano",
        "copaDasEstrelas": "Copa das estrelas"
    }
    return nomes.get(nome, nome)

def wait_and_click(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        element.click()
        return True
    except Exception as e:
        print(f"[WARNING] Elemento não clicável: ({by}, {value}) - {e}")
        return False

def get_html(campeonato):
    url = "https://www.betano.bet.br/virtuals/futebol/"
    liga = format_name(campeonato)

    options = Options()

    driver = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        options=options
    )

    try:
        driver.get(url)
        print(f"[INFO] Acessando: {url}")

        if not wait_and_click(driver, By.XPATH, '//button[span[text()="Sim"]]'): return None
        if not wait_and_click(driver, By.CSS_SELECTOR, 'button[type="button"]'): return None
        if not wait_and_click(driver, By.LINK_TEXT, liga): return None
        if not wait_and_click(driver, By.LINK_TEXT, liga): return None
        if not wait_and_click(driver, By.CSS_SELECTOR, "div[data-qa='virtuals-results-toggle-button']"): return None

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
                ".tw-flex.tw-items-center.tw-justify-center.tw-mt-m.tw-mb-n.tw-mx-n"))
        )

        return driver.page_source

    except Exception as e:
        print(f"[ERRO] Erro no scraping de {campeonato}: {e}")
        return None

    finally:
        driver.quit()
