import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pygame

count_alarm = 0
erros_anterior = 0
acertos = 0
erros = 0
driver = None  # Variável global para o driver

# Redefine o caminho da área de trabalho para o sistema operacional
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")


service = Service()
options = webdriver.ChromeOptions()
# Remova a opção --headless para tornar o navegador visível
options.add_argument("--headless")
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


def extrair_cores_25(driver):
    # Abrir o site se ainda não estiver aberto
    if driver.current_url != "https://blaze-7.com/pt/games/double?modal=double_history_index":
        driver.get(
            "https://blaze-7.com/pt/games/double?modal=double_history_index")
        time.sleep(1)

        # Esperar até que a div "tabs-crash-analytics" esteja visível
        tabs_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "tabs-crash-analytics")))

        # Clicar no botão "Padrões" dentro da div "tabs-crash-analytics"
        padroes_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//button[text()='Padrões']")))
        padroes_button.click()

        # Esperar até que o botão "Padrões" se torne ativo
        padroes_active_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='tab active']")))

    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@tabindex='0']")))
    select = Select(select_element)

    time.sleep(2)
    select.select_by_value("50")

    time.sleep(2)
    select.select_by_value("25")

    time.sleep(2)

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



def verificar_padrao(sequencia):
    count_cores_iguais = 1
    cor_anterior = sequencia[0]
    for cor_atual in sequencia[1:]:
        if cor_atual == cor_anterior:
            count_cores_iguais += 1
            if count_cores_iguais >= 5:
                return "erro"  # Se encontrar 5 ou mais cores iguais em sequência, retorna erro
        else:
            count_cores_iguais = 1
            cor_anterior = cor_atual
    return "acerto"  # Se não encontrar 5 ou mais cores iguais em sequência, retorna acerto


def main():
    global erros_anterior
    global driver
    global count_alarm
    global acertos
    global erros
    global last_alarm_time
    global padrao

    last_alarm_time = time.time()  # Inicializa o tempo do último alarme
    sequencia_anterior = []  # Inicializa a sequência anterior como vazia

    try:
        url = 'https://blaze-7.com/pt/games/double'
        driver.get(url)

        while not verificar_stop():
            recent_results_element = driver.find_element(
                By.ID, "roulette-recent")
            box_elements = recent_results_element.find_elements(
                By.CLASS_NAME, "sm-box")

            sequencia = [box_element.get_attribute(
                "class").split()[-1] for box_element in box_elements[:3]]
            percentuais = extrair_cores_25(driver)

            print("Ultimos 3 resultados:", sequencia)
            print("")

            # Verifica o padrão da sequência atual
            padrao = verificar_padrao(sequencia)

            if count_alarm > 0:
                # Se o alarme já tiver sido acionado, verificar a sequência atual
                if padrao == "erro":
                    # Se encontrar uma quebra de padrão após o alarme, incrementa o contador de erros
                    erros_anterior += 1
                else:
                    # Se a sequência atual não quebrar o padrão, reinicia o contador de erros
                    erros_anterior = 0

                if erros_anterior >= 5:
                    # Se houverem 5 ou mais quebras de padrão consecutivas após o alarme, reinicia o contador do alarme
                    count_alarm = 0
                    erros_anterior = 0

            if len(set(sequencia)) == 1:
                # Sequência de 3 cores iguais
                cor_atual = sequencia[0]
                cor_oposta = None
                if cor_atual == 'red':
                    cor_oposta = 'black'
                elif cor_atual == 'black':
                    cor_oposta = 'red'
                if cor_oposta:
                    # Obtém o percentual da cor oposta
                    percentual_oposto = int(
                        percentuais[['white', 'black', 'red'].index(cor_oposta)])

                    if percentual_oposto is not None:
                        if percentual_oposto <= 42:

                            current_time = time.time()
                            if current_time - last_alarm_time >= 60:  # Verifica se passaram 60 segundos desde o último alarme
                                alarm_sound.play()

                                count_alarm += 1  # Incrementa o contador

                                print(f"Alarme acionado. Contagem: {
                                      count_alarm}")  # Imprime a contagem

                                last_alarm_time = current_time  # Atualiza o tempo do último alarme

            if count_alarm > 0:
                # Verifica se a sequência atual quebra o padrão após o alarme
                if padrao == "acerto":
                    acertos += 1  # Incrementa a contagem de acertos
                else:
                    erros += 1  # Incrementa a contagem de erros

            time.sleep(2)

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
