from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

# Configurações do ChromeDriver
service = Service()
options = webdriver.ChromeOptions()

# Caminho para a área de trabalho
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Caminho completo do arquivo .txt na área de trabalho
txt_file_path = os.path.join(desktop_path, "resultados double.txt")

# Limitar o número de páginas a serem extraídas
limite_paginas = 10

# Loop infinito para manter o script em execução
while True:
    try:
        # Configurações do WebDriver
        driver = webdriver.Chrome(service=service, options=options)

        url = 'https://blaze-7.com/pt/games/double?modal=double_history_index'
        driver.get(url)

        # Encontrar todos os botões de paginação
        botoes_paginacao = driver.find_elements(
            By.CLASS_NAME, "pagination__button")

        # Encontrar o botão de retrocesso (primeiro botão dentro de pagination-group)
        botao_retrocesso = None
        for botao in botoes_paginacao:
            if "pagination-group" in botao.get_attribute("class"):
                botao_retrocesso = botao.find_elements(
                    By.CLASS_NAME, "pagination__button")[0]
                break

        # Inicializar variável para a página atual
        pagina_atual = limite_paginas

        # Loop para extrair resultados de várias páginas
        for _ in range(limite_paginas):
            # Atualizar a URL para a página desejada
            url_pagina = f"{url}&page={pagina_atual}"
            driver.get(url_pagina)

            # Encontrar o elemento pelo ID 'history__double'
            history_element = driver.find_element(By.ID, "history__double")

            # Encontrar todos os contêineres 'history__double__container' dentro do elemento 'history__double'
            container_elements = history_element.find_elements(
                By.CLASS_NAME, "history__double__container")

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

                    # Imprimir no console
                    print(f"Número: {number}, Cor: {color}")

                    # Escrever no arquivo .txt
                    txt_file.write(f"Número: {number}, Cor: {color}\n")

            # Decrementar a página atual para navegar para a próxima página
            pagina_atual -= 1

            # Clicar no botão de retrocesso
            botao_retrocesso.click()

            # Aguardar um curto intervalo antes de passar para a próxima página
            time.sleep(5)  # Pode ajustar conforme necessário

        # Reiniciar o navegador
        driver.quit()

    except Exception as e:
        print(f"Erro: {e}")
        # Aguardar um intervalo curto antes de tentar novamente
        time.sleep(15)  # 15 segundos
