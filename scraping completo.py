from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time
from datetime import datetime

# Configurações do ChromeDriver
service = Service()
options = webdriver.ChromeOptions()

# Executar em modo headless (sem interface gráfica)
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# Desativar carregamento de imagens para acelerar o processo
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

# Caminho para a área de trabalho
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Caminho completo do arquivo .txt na área de trabalho
txt_file_path = os.path.join(desktop_path, "resultados double.txt")

# Limitar o número de páginas a serem extraídas
limite_paginas = 288

# Iniciar o WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navegar até a décima página
    url = 'https://blaze-7.com/pt/games/double?modal=double_history_index'
    driver.get(url)

    # Clicar no botão de avanço nas páginas para ir até a décima página
    for _ in range(287):
        botao_avanco = driver.find_elements(
            By.CLASS_NAME, "pagination__button")[1]
        botao_avanco.click()
        time.sleep(1)  # Aguardar um curto intervalo entre os cliques

    # Loop para retroceder e extrair as páginas
    for _ in range(limite_paginas):
        # Encontrar o elemento pelo ID 'history__double'
        history_element = driver.find_element(By.ID, "history__double")

        # Encontrar todos os contêineres 'history__double__container' dentro do elemento 'history__double'
        container_elements = history_element.find_elements(
            By.CLASS_NAME, "history__double__container")

        # Inverter a ordem dos contêineres
        container_elements.reverse()

        # Processar cada contêiner para extrair informações
        with open(txt_file_path, "a") as txt_file:
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

                # Encontrar o elemento de data e hora
                date_element = container_element.find_element(
                    By.CLASS_NAME, "history__double__date")

                # Obter a segunda linha do elemento, que contém a hora
                time_text = date_element.text.split('\n')[1]

                # Concatenar os resultados em uma única linha
                result_line = f"Número: {number}, Cor: {color} - {time_text}"

                # Imprimir no console
                print(result_line)

                # Escrever no arquivo .txt
                txt_file.write(result_line + "\n")

        # Clicar no botão de retrocesso
        botao_retrocesso = driver.find_elements(
            By.CLASS_NAME, "pagination__button")[0]
        botao_retrocesso.click()

        # Aguardar um curto intervalo antes de passar para a próxima página
        time.sleep(2)  # Pode ajustar conforme necessário

except Exception as e:
    print(f"Erro: {e}")

finally:
    # Fechar o navegador
    driver.quit()
