from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def dataAtualizacao():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def Format_name(text):
    match text:
        case "copaAmerica":
            return "Copa America"
        case "tacaGloriaEterna":
            return "Taça Glória eterna"
        case "euro":
            return "Euro"
        case "britishDerbies":
            return "British Derbies"
        case "ligaEspanhola":
            return "Liga Espanhola"
        case "scudettoItaliano":
            return "Scudetto Italiano"
        case "campeonatoItaliano":
            return "Campeonato Italiano"
        case "copaDasEstrelas":
            return "Copa das estrelas"

def get_html(campeonato):
    url = "https://www.betano.bet.br/virtuals/futebol/"
    liga = Format_name(campeonato)

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("User-Agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        options=options
    )

    try:
        print(f"[INFO] Acessando: {url}")
        driver.get(url)

        try:
            # Usa o seletor pelo atributo `data-qa`
            button_sim = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-qa="age-verification-modal-ok-button"]'))
            )
            button_sim.click()
        except Exception as e:
            print(f"[WARNING] Falha ao clicar em botão 'Sim': {e}")
            driver.save_screenshot(f"error_{campeonato}_sim.png")
            return None

        try:
            # Botão X para fechar modal
            button_x = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"]'))
            )
            button_x.click()
        except Exception as e:
            print(f"[WARNING] Falha ao clicar em botão 'X': {e}")
            driver.save_screenshot(f"error_{campeonato}_x.png")
            return None

        try:
            camp = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, f"{liga}"))
            )
            camp.click()
            camp.click()
        except Exception as e:
            print(f"[WARNING] Falha ao clicar em campeonato '{liga}': {e}")
            driver.save_screenshot(f"error_{campeonato}_liga.png")
            return None

        try:
            button_results = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-qa='virtuals-results-toggle-button']"))
            )
            button_results.click()
        except Exception as e:
            print(f"[WARNING] Falha ao clicar em botão de resultados: {e}")
            driver.save_screenshot(f"error_{campeonato}_resultados.png")
            return None

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 
                ".tw-flex.tw-items-center.tw-justify-center.tw-mt-m.tw-mb-n.tw-mx-n"))
        )

        print(f"[INFO] HTML capturado com sucesso para {campeonato}")
        return driver.page_source

    except Exception as e:
        print(f"[ERRO] Falha inesperada em {campeonato}: {e}")
        driver.save_screenshot(f"error_{campeonato}_geral.png")
        return None

    finally:
        driver.quit()
