from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

# Configurações do ChromeDriver
service = Service('/path/to/chromedriver')  # Substitua pelo caminho do seu chromedriver
options = webdriver.ChromeOptions()

# Executar em modo headless (sem interface gráfica)
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')

# Desativar carregamento de imagens para acelerar o processo
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

# Caminho para a área de trabalho
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Caminho completo do arquivo .txt na área de trabalho
txt_file_path = os.path.join(desktop_path, "resultados_bets.txt")

# URL base
base_url = 'https://blaze1.space/pt/games/crash?modal=crash_history_index'

# Iniciar o WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navegar até a página inicial do histórico de apostas
    driver.get(base_url)
    time.sleep(3)  # Aguardar o carregamento completo da página

    # Retroceder até a primeira página
    pagination_buttons = driver.find_elements(By.CLASS_NAME, "pagination__button")
    last_page_button = pagination_buttons[-1]

    # Loop para retroceder e extrair todas as páginas
    while True:
        # Encontrar todos os elementos de aposta 'bet'
        bet_elements = driver.find_elements(By.CLASS_NAME, "bet")

        # Processar cada elemento de aposta para extrair informações
        with open(txt_file_path, "a", encoding="utf-8") as txt_file:
            for bet_element in bet_elements:
                try:
                    # Encontrar o elemento de multiplicador dentro do contêiner da aposta
                    multiplier_element = bet_element.find_element(By.CLASS_NAME, "bet-amount")
                    multiplier = multiplier_element.text

                    # Encontrar o elemento de data e hora
                    datetime_element = bet_element.find_element(By.TAG_NAME, "p")
                    datetime_text = datetime_element.text

                    # Concatenar os resultados em uma única linha
                    result_line = f"Multiplicador: {multiplier} - {datetime_text}"

                    # Imprimir no console
                    print(result_line)

                    # Escrever no arquivo .txt
                    txt_file.write(result_line + "\n")
                except Exception as e:
                    print(f"Erro ao processar aposta: {e}")

        # Verificar se há um botão de retrocesso
        if "pagination__button--prev" in last_page_button.get_attribute("class"):
            last_page_button.click()
            time.sleep(3)  # Aguardar o carregamento completo da página
        else:
            break  # Se não houver mais páginas para retroceder, sair do loop

except Exception as e:
    print(f"Erro: {e}")

finally:
    # Fechar o navegador
    driver.quit()
