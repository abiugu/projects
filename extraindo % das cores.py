from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# Configuração do serviço e do webdriver para executar em modo headless
service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Executar em modo headless
options.add_argument("--start-maximized")  # Maximizar a janela do navegador
driver = webdriver.Chrome(service=service, options=options)

# Abrir o site
driver.get("https://blaze-7.com/pt/games/double?modal=double_history_index")

# Esperar até que a div "tabs-crash-analytics" esteja visível
tabs_div = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "tabs-crash-analytics")))

# Clicar no botão "Padrões" dentro da div "tabs-crash-analytics"
padroes_button = tabs_div.find_element(By.XPATH, ".//button[text()='Padrões']")
padroes_button.click()

# Esperar até que o botão "Padrões" se torne ativo
padroes_active_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//button[@class='tab active']")))

# Selecionar o valor de 25 nas últimas rodadas
select_element = driver.find_element(By.XPATH, "//select[@tabindex='0']")
select = Select(select_element)

select.select_by_value("50")

# Esperar até que os elementos de texto estejam presentes na página
text_elements_present = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "text")))

# Aguardar até que os elementos de texto estejam visíveis na página
text_elements_visible = WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located((By.TAG_NAME, "text")))

# Extrair os valores das últimas 50 rodadas
valores_50 = [element.get_attribute("textContent") for element in text_elements_present 
              if element.get_attribute("y") == "288" and "SofiaPro" in element.get_attribute("font-family")]


select.select_by_value("25")

# Aguardar 1 segundo após selecionar as últimas 25 rodadas
time.sleep(1)

# Encontrar todos os elementos de texto
text_elements = driver.find_elements(By.TAG_NAME, "text")

# Filtrar os elementos que têm a coordenada y igual a 288 e a fonte SofiaPro
valores_25 = [element.get_attribute("textContent") for element in text_elements
              if element.get_attribute("y") == "288" and "SofiaPro" in element.get_attribute("font-family")]

# Imprimir os valores extraídos com a indicação das últimas 25 rodadas
print("Ultimas 25 rodadas:", valores_25)
print("Ultimas 50 rodadas:", valores_50)

# Fechar o navegador
driver.quit()
