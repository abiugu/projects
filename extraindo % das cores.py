from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do webdriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Maximiza a janela do navegador
driver = webdriver.Chrome(options=options)

# Abrir o site
driver.get("https://blaze-7.com/pt/games/double?modal=double_history_index")

# Esperar até que o botão de histórico esteja disponível e clicar nele
history_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "buttons-history")))
history_button.click()

# Clicar no botão "Padrões"
padroes_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='Padrões']")))
padroes_button.click()

# Esperar até que o botão "Padrões" se torne ativo
padroes_active_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//button[@class='tab active']")))

# Selecionar o valor de 50 nas últimas 50 rodadas
select_menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, "//div[@class='select-menu']//select")))
select_menu.find_element_by_css_selector("option[value='50']").click()

# Extrair os valores de texto nas coordenadas y="288" e font-family="SofiaPro"
valores = []
texts = driver.find_elements_by_xpath(
    "//text[@y='288' and @font-family='SofiaPro']")
for text in texts:
    valores.append(text.text)

print(valores)  # Imprime os valores extraídos

# Fechar o navegador
driver.quit()
