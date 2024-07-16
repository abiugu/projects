from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from alerta1 import alarme_acionado  # Supondo que alarme_acionado seja uma função que verifica o alarme

# Configurando o serviço do Chrome
chrome_service = Service()  # Substitua pelo caminho do seu chromedriver

# Configurando as opções do Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Executar em modo headless (sem interface gráfica)

# Inicializando o driver do Chrome
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    while True:
        # Abrindo o link desejado
        driver.get("https://blaze1.space/pt/games/double?modal=auth&tab=login")

        # Esperar até que o link inicial carregue completamente
        WebDriverWait(driver, 10).until(EC.url_to_be("https://blaze1.space/pt/games/double?modal=auth&tab=login"))

        # Definir a URL inicial
        url_inicial = driver.current_url

        # Monitorar se a URL mudou para algo diferente da URL inicial
        while True:
            current_url = driver.current_url
            if current_url != url_inicial:
                print(f"URL mudou para: {current_url}")
                break
            time.sleep(1)  # Verificar a cada segundo se a URL mudou

        driver.get("https://blaze1.space/pt/games/double?modal=double_history_index")

        # Aguardando até que o elemento da última jogada esteja presente na página
        last_play_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".entries.main .entry .roulette-tile .sm-box"))
        )

        # Obtendo o estilo de cor do elemento
        style_attribute = last_play_element.get_attribute("style")

        # Verificando a cor baseada no estilo
        if "red" in style_attribute:
            cor_ultima_jogada = "red"
        elif "black" in style_attribute:
            cor_ultima_jogada = "black"
        elif "white" in style_attribute:
            cor_ultima_jogada = "white"
        else:
            cor_ultima_jogada = "cor não reconhecida"

        if alarme_acionado():  # Verificar se o alarme foi acionado

            if cor_ultima_jogada == "red":
                # Escolher a cor preta
                cor_black_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.black.selected")))
                cor_black_button.click()

            elif cor_ultima_jogada == "black":
                # Escolher a cor vermelha
                cor_red_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.red.selected")))
                cor_red_button.click()

            # Inserir o valor no campo de Quantia
            valor_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.input-field-wrapper input.input-field")))
            driver.execute_script("arguments[0].setAttribute('value', '1.00');", valor_field)

            # Clicar no botão "Começar o jogo"
            comecar_jogo_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.place-bet button")))
            comecar_jogo_button.click()

except KeyboardInterrupt:
    print("\nPrograma encerrado pelo usuário.")

except Exception as e:
    print(f"Erro ao tentar realizar a entrada: {e}")

finally:
    # Manter o navegador aberto por um tempo para permitir verificação manual
    input("Pressione Enter para fechar o navegador...")

    # Fechar o navegador
    driver.quit()
