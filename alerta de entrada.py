import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pygame

# Redefine o caminho da área de trabalho para o sistema operacional
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Inicializa o mixer de áudio do pygame
pygame.mixer.init()

# Carrega o arquivo de som
sound_file_path = "MONEY ALARM.mp3"
# Carrega o som
alarm_sound = pygame.mixer.Sound(sound_file_path)


def verificar_stop():
    stop_path = os.path.join(desktop_path, "stop.txt")
    return os.path.exists(stop_path)


def extrair_cores_25(driver):
    # Atualizar a página para obter as informações mais recentes
    driver.refresh()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "roulette-recent")))
    recent_results_element = driver.find_element(By.ID, "roulette-recent")
    box_elements = recent_results_element.find_elements(
        By.CLASS_NAME, "sm-box")
    sequencia = [box_element.get_attribute(
        "class").split()[-1] for box_element in box_elements[:3]]
    print("Ultimos 3 resultados:", sequencia)

    # Extrair as porcentagens
    text_elements_present = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "text")))
    text_elements_visible = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.TAG_NAME, "text")))
    valores_25 = [element.get_attribute("textContent") for element in text_elements_present if element.get_attribute(
        "y") == "288" and "SofiaPro" in element.get_attribute("font-family")]
    percentuais = [int(valor.split('%')[0]) for valor in valores_25]

    log_result = "Ultimas 25 rodadas: " + ', '.join(map(str, percentuais))
    print(log_result)

    return sequencia, percentuais


def main():
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Executar em modo headless
    # Maximizar a janela do navegador
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = 'https://blaze-7.com/pt/games/double'
        driver.get(url)

        while not verificar_stop():
            sequencia, percentuais = extrair_cores_25(driver)

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
                    percentual_atual = percentuais[[
                        'white', 'black', 'red'].index(cor_atual)]
                    if percentual_atual is not None and percentual_atual <= 38:
                        alarm_sound.play()

            time.sleep(2)  # Aguarda 2 segundos antes de atualizar novamente

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
