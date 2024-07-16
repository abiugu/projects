from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurando o serviço do Chrome
chrome_service = Service('Caminho_para_seu_chromedriver.exe')  # Substitua pelo caminho do seu chromedriver

# Configurando as opções do Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar em modo headless (sem interface gráfica)

# Inicializando o driver do Chrome
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    # Abrindo o link desejado
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

    print(f"A última jogada foi: {cor_ultima_jogada}")

finally:
    # Fechando o navegador
    driver.quit()
