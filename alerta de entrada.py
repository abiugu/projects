import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pygame

service = Service()
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Executar em modo headless
# options.add_argument("--start-maximized")  # Maximizar a janela do navegador
driver = webdriver.Chrome(service=service, options=options)

count_alarm = 0
erros_anterior = 0
acertos = 0
erros = 0
last_alarm_time = 0  # Inicializar last_alarm_time


# Redefine o caminho da área de trabalho para o sistema operacional
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Caminho completo para o arquivo de log
log_file_path = os.path.join(desktop_path, "log.txt")

# Inicializa o mixer de áudio do pygame
pygame.mixer.init()

# Carrega o arquivo de som
sound_file_path = "MONEY ALARM.mp3"

# Carrega o som
alarm_sound = pygame.mixer.Sound(sound_file_path)


def log_to_file(message):
    with open(log_file_path, "a") as log_file:
        log_file.write(message + "\n")


def verificar_stop():
    stop_path = os.path.join(desktop_path, "stop.txt")
    return os.path.exists(stop_path)


def extrair_cores_25(driver):
    # Abrir o site se ainda não estiver aberto
    if driver.current_url != "https://blaze1.space/pt/games/double?modal=double_history_index":
        driver.get(
            "https://blaze1.space/pt/games/double?modal=double_history_index")
        # Aguarda até 5 segundos para elementos aparecerem
        driver.implicitly_wait(5)

        # Esperar até que a div "tabs-crash-analytics" esteja visível
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "tabs-crash-analytics")))

        # Clicar no botão "Padrões" dentro da div "tabs-crash-analytics"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//button[text()='Padrões']"))).click()

        # Esperar até que o botão "Padrões" se torne ativo
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='tab active']")))

    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@tabindex='0']")))
    select = Select(select_element)
    driver.implicitly_wait(3)
    select.select_by_value("50")
    driver.implicitly_wait(3)
    select.select_by_value("25")
    driver.implicitly_wait(3)

    text_elements_present = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "text")))
    text_elements_visible = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.TAG_NAME, "text")))
    valores_25 = [element.get_attribute("textContent") for element in text_elements_present
                  if element.get_attribute("y") == "288" and "SofiaPro" in element.get_attribute("font-family")]

    # Extrair apenas os valores de porcentagem e remover o símbolo '%'
    percentuais = [valor.split('%')[0] for valor in valores_25]

    log_result = "Ultimas 25 rodadas: " + ', '.join(percentuais)
    log_to_file(log_result)  # Adiciona o resultado ao log
    return percentuais


def verificar_padrao(sequencia, cor_atual_percentual):
    global acertos
    global erros

    count_cores_iguais = 1
    cor_anterior = sequencia[0]
    for cor_atual in sequencia[1:]:
        if cor_atual == cor_anterior:
            count_cores_iguais += 1
            if count_cores_iguais == 4:
                # Verifica se a próxima cor é a mesma
                if cor_atual == sequencia[sequencia.index(cor_atual) + 1]:
                    erros += 1
                else:
                    acertos += 1
                break
        else:
            count_cores_iguais = 1
        cor_anterior = cor_atual


def main():
    global erros_anterior
    global driver
    global count_alarm
    global acertos
    global erros
    global last_alarm_time
    global sequencia_anterior

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

            if sequencia != sequencia_anterior:  # Verifica se há uma nova sequência
                percentuais = extrair_cores_25(driver)
                log_to_file("Ultimos 3 resultados: " + ', '.join(sequencia))

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
                        cor_atual_percentual = int(
                            percentuais[['white', 'black', 'red'].index(cor_atual)])

                        if cor_atual_percentual is not None:
                            if cor_atual_percentual <= 36:
                                current_time = time.time()
                                if current_time - last_alarm_time >= 60:  # Verifica se passaram 60 segundos desde o último alarme
                                    alarm_sound.play()
                                    count_alarm += 1  # Incrementa o contador
                                    print(f"Alarme acionado. Contagem: {
                                        count_alarm}")  # Imprime a contagem
                                    log_to_file(
                                        f"Alarme acionado. Contagem: {count_alarm}")
                                    last_alarm_time = current_time  # Atualiza o tempo do último alarme

                if len(set(sequencia)) == 1:
                    verificar_padrao(sequencia, cor_atual_percentual)

                sequencia_anterior = sequencia  # Atualiza a sequência anterior

            # Aguarda 1 segundo antes de verificar novamente
            time.sleep(1)

    except Exception as e:
        error_message = f"Erro: {e}"
        print(error_message)
        log_to_file(error_message)  # Adiciona o erro ao log

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
