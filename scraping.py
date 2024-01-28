from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os



# Configurações do ChromeDriver
service = Service()
options = webdriver.ChromeOptions()

# Caminho para a área de trabalho
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Configurações do WebDriver
driver = webdriver.Chrome(service=service, options=options)

url = 'https://blaze-7.com/pt/games/double?modal=double_history_index'
driver.get(url)

# Encontrar o elemento pelo ID 'history__double'
history_element = driver.find_element(By.ID, "history__double")

# Encontrar todos os contêineres 'history__double__container' dentro do elemento 'history__double'
container_elements = history_element.find_elements(
    By.CLASS_NAME, "history__double__container")

# Caminho completo do arquivo .txt na área de trabalho
txt_file_path = os.path.join(desktop_path, "resultados double.txt")

# Processar cada contêiner para extrair informações
with open(txt_file_path, "w") as txt_file:
    for container_element in container_elements:
        # Encontrar o elemento de cor dentro do contêiner
        color_element = container_element.find_element(
            By.CLASS_NAME, "history__double__item")

        # Verificar a classe do elemento para determinar a cor
        if "history__double__item--black" in color_element.get_attribute("class"):
            color = "black"
        elif "history__double__item--white" in color_element.get_attribute("class"):
            color = "white"
        elif "history__double__item--red" in color_element.get_attribute("class"):
            color = "red"
        else:
            color = "unknown"

        # Encontrar o número dentro da classe 'history__double__center'
        number_element = color_element.find_element(
            By.CLASS_NAME, "history__double__center")
        number = number_element.text

        # Imprimir no console
        print(f"Número: {number}, Cor: {color}")

        # Escrever no arquivo .txt
        txt_file.write(f"Número: {number}, Cor: {color}\n")

# Fechar o navegador
driver.quit()
