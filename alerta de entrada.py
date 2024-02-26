import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pygame

erros_anterior = 0
driver = None  # Variável global para o driver

# Redefine o caminho da área de trabalho para o sistema operacional
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Executar em modo headless
options.add_argument("--start-maximized")  # Maximizar a janela do navegador
driver = webdriver.Chrome(service=service, options=options)

# Inicializa o mixer de áudio do pygame
pygame.mixer.init()

# Carrega o arquivo de som
sound_file_path = "MONEY ALARM.mp3"

# Carrega o som
alarm_sound = pygame.mixer.Sound(sound_file_path)


def verificar_stop():
    stop_path = os.path.join(desktop_path, "stop.txt")
    return os.path.exists(stop_path)


def somar_resultados(sequencia):
    global erros_anterior

    cores_anteriores = sequencia[1:4]
    cor_atual = sequencia[0]

    return


def extrair_cores_25():
    global driver

    # Abrir o site se ainda não estiver aberto
    if driver.current_url != "https://blaze-7.com/pt/games/double?modal=double_history_index":
        driver.get(
            "https://blaze-7.com/pt/games/double?modal=double_history_index")
        # Esperar até que a div "tabs-crash-analytics" esteja visível
        tabs_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "tabs-crash-analytics")))
        # Clicar no botão "Padrões" dentro da div "tabs-crash-analytics"
        padroes_button = tabs_div.find_element(
            By.XPATH, ".//button[text()='Padrões']")
        padroes_button.click()
        # Esperar até que o botão "Padrões" se torne ativo
        padroes_active_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='tab active']")))

    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@tabindex='0']")))
    select = Select(select_element)

    time.sleep(1)

    select.select_by_value("50")

    time.sleep(1)

    select.select_by_value("25")

    time.sleep(1)

    text_elements_present = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "text")))
    text_elements_visible = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.TAG_NAME, "text")))
    valores_25 = [element.get_attribute("textContent") for element in text_elements_present
                  if element.get_attribute("y") == "288" and "SofiaPro" in element.get_attribute("font-family")]

    # Extrair apenas os valores de porcentagem e remover o símbolo '%'
    percentuais = [valor.split('%')[0] for valor in valores_25]

    log_result = "Ultimas 25 rodadas: " + ', '.join(percentuais)
    print(log_result)
    return percentuais



def main():
    global erros_anterior
    global driver

    try:
        driver = webdriver.Chrome(service=service, options=options)
        url = 'https://blaze-7.com/pt/games/double'
        driver.get(url)

        while not verificar_stop():
            recent_results_element = driver.find_element(
                By.ID, "roulette-recent")
            box_elements = recent_results_element.find_elements(
                By.CLASS_NAME, "sm-box")

            sequencia = [box_element.get_attribute(
                "class").split()[-1] for box_element in box_elements[:3]]

            percentuais = extrair_cores_25()

            print("Ultimos 3 resultados:", sequencia)
            print("")

        if len(set(sequencia)) == 1:
    # Sequência de 3 cores iguais
            cor_atual = sequencia[0]
            if cor_atual == 'red':
                cor_oposta = 'black'
            elif cor_atual == 'black':
                cor_oposta = 'red'
            else:
                cor_oposta = None  # Se a sequência não for vermelha nem preta, não faz sentido verificar
            if cor_oposta:
                percentual_oposto = int(percentuais[['white', 'black', 'red'].index(cor_oposta)])
                percentual_atual = int(percentuais[['white', 'black', 'red'].index(cor_atual)])
                if percentual_oposto is not None and percentual_atual is not None:
                    if percentual_oposto <= 52 and percentual_atual <= 38:
                        alarm_sound.play()




            time.sleep(1)

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
