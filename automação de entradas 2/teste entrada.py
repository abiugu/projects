import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select



service = Service()
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Executar em modo headless
options.add_argument("--start-maximized")  # Maximizar a janela do navegador
driver = webdriver.Chrome(service=service, options=options)

count_alarm = 0
acertos_direto = 0
acertos_gale = 0
erros = 0
last_alarm_time = 0  # Inicializar last_alarm_time
alarme_acionado = False  # Inicializa o estado do alarme como falso

# Redefine o caminho da área de trabalho para o sistema operacional
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")



def verificar_stop():
    stop_path = os.path.join(desktop_path, "stop.txt")
    return os.path.exists(stop_path)


def login(driver):
    driver.get("https://blaze1.space/pt/games/double?modal=auth&tab=login")
    driver.find_element(By.NAME, 'username').send_keys("abiugu@gmail.com")
    driver.find_element(By.NAME, 'password').send_keys("Abiugu0203@")
    driver.find_element(By.CSS_SELECTOR, 'button.red.submit.shared-button-custom').click()
    print("Login efetuado com sucesso!")

def extrair_cores(driver, valor):
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
    time.sleep(2)
    select.select_by_value(str(valor))
    time.sleep(2)

    text_elements_present = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "text")))

    # Extrair apenas os valores de porcentagem e remover o símbolo '%'
    valores = [element.get_attribute("textContent") for element in text_elements_present
               if element.get_attribute("y") == "288" and "SofiaPro" in element.get_attribute("font-family")]
    percentuais = [float(valor.split('%')[0]) for valor in valores]

    return percentuais

def obter_cor_oposta(cor_atual):
    return 'red' if cor_atual == 'black' else 'black'

def apostar(driver, obter_cor_aposta, valor):
    # Clicar no botão da cor para selecioná-la
    # Assume que a cor passada é 'red', 'black' ou 'white'
    cor_seletor = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'div.input-wrapper.select div.{obter_cor_aposta}'))
    )
    cor_seletor.click()
    print(f"Cor {obter_cor_aposta} selecionada com sucesso!")

    # Ajustar o valor da aposta no campo correspondente
    campo_quantidade = driver.find_element(By.CSS_SELECTOR, '.balance-input-field .input-field')
    campo_quantidade.clear()
    campo_quantidade.send_keys(str(valor))
    
    # Clicar no botão para realizar a aposta
    botao_aposta = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'button.shared-button-custom[data-bet="{obter_cor_aposta}"]'))
    )
    botao_aposta.click()
    print(f"Aposta de {valor} na cor {obter_cor_aposta} realizada com sucesso!")

def main():
    global count_alarm
    global acertos_direto
    global acertos_gale
    global erros
    global last_alarm_time
    global alarme_acionado
    global sequencia
    sequencia_anterior = []  # Definindo a variável sequencia_anterior antes de ser utilizada

    last_alarm_time = time.time()  # Inicializa o tempo do último alarme

    try:
        url = 'https://blaze-7.com/pt/games/double'
        driver.get(url)

        while not verificar_stop():
            recent_results_element = driver.find_element(
                By.ID, "roulette-recent")
            box_elements = recent_results_element.find_elements(
                By.CLASS_NAME, "sm-box")

            # Analisa as 15 últimas cores disponíveis
            sequencia = [box_element.get_attribute(
                "class").split()[-1] for box_element in box_elements[:15]]

            # Obtém apenas as últimas 3 cores para imprimir
            ultimas_tres_cores = sequencia[:3]

            # Verifica se houve uma mudança na sequência de cores
            if sequencia != sequencia_anterior:

                # Verifica se há alguma sequência de 3 cores iguais
                if len(set(ultimas_tres_cores)) == 1:
                    percentuais100 = extrair_cores(driver, 100)
                    percentuais25 = extrair_cores(driver, 25)
                    percentuais500 = extrair_cores(driver, 500)
                    cor_atual = sequencia[0]
                    cor_oposta = None
                    if cor_atual == 'red':
                        cor_oposta = 'black'
                    elif cor_atual == 'black':
                        cor_oposta = 'red'
                    if cor_oposta:

                        cor_atual_percentual_500 = int(
                            percentuais500[['white', 'black', 'red'].index(cor_atual)])
                        cor_oposta_percentual_500 = int(
                            percentuais500[['white', 'black', 'red'].index(cor_oposta)])
                        
                        cor_atual_percentual_100 = int(
                            percentuais100[['white', 'black', 'red'].index(cor_atual)])
                        cor_oposta_percentual_100 = int(
                            percentuais100[['white', 'black', 'red'].index(cor_oposta)])
                        
                        cor_atual_percentual_25 = int(
                            percentuais25[['white', 'black', 'red'].index(cor_atual)])

                        if cor_atual_percentual_25 is not None:
                            print(f"Cor atual: {cor_atual}, Percentual: {
                                  cor_atual_percentual_25}")

                            if cor_atual_percentual_25 <= 48 and cor_atual_percentual_100 >= cor_oposta_percentual_100 and cor_atual_percentual_500 <= cor_oposta_percentual_500:
                                if ultimas_tres_cores[0] == ultimas_tres_cores[1] == ultimas_tres_cores[2]:
                                    print(
                                        "Três cores iguais e padrão encontrado. Solicitar alarme.")
                                    current_time = time.time()
                                    if current_time - last_alarm_time >= 60:
                                        count_alarm += 1
                                        print(f"Alarme acionado. Contagem: {
                                              count_alarm}")
                                        last_alarm_time = current_time
                                        alarme_acionado = True  # Define alarme_acionado como True

                sequencia_anterior = sequencia  # Atualiza a sequência anterior

            # Lógica para verificar duas sequências após o alarme acionado
                def obter_ultimas_tres_cores(driver):
                    recent_results_element = driver.find_element(By.ID, "roulette-recent")
                    box_elements = recent_results_element.find_elements(By.CLASS_NAME, "sm-box")
                    sequencia = [box_element.get_attribute("class").split()[-1] for box_element in box_elements[:3]]
                    return sequencia

                if alarme_acionado:
                        while not os.path.exists(os.path.join(os.path.expanduser("~"), "Desktop", "stop.txt")):
                            if sequencia_anterior[0] == obter_ultimas_tres_cores(driver)[0]:
                                apostar(driver, obter_cor_oposta(sequencia_anterior[0]), 0.50)
                                apostar(driver, 'white', 0.10)
                                time.sleep(20)  # Espera o resultado da rodada
                
                                if obter_ultimas_tres_cores(driver)[0] == sequencia_anterior[0]:
                                    apostar(driver, obter_cor_oposta(sequencia_anterior[0]), 1.00)
                                    apostar(driver, 'white', 0.20)
                                    time.sleep(10)  # Pequena pausa antes de verificar novamente

                if sequencia != sequencia_anterior:
                        
                    recent_results_element = driver.find_element(
                        By.ID, "roulette-recent")
                    box_elements = recent_results_element.find_elements(
                        By.CLASS_NAME, "sm-box")
                    sequencia_1 = [box_element.get_attribute(
                        "class").split()[-1] for box_element in box_elements[:15]]
                    ultimas_tres_cores_1 = sequencia_1[:3]


                    while ultimas_tres_cores_1 == sequencia_1:
                        recent_results_element = driver.find_element(
                            By.ID, "roulette-recent")
                        box_elements = recent_results_element.find_elements(
                            By.CLASS_NAME, "sm-box")
                        sequencia = [box_element.get_attribute(
                            "class").split()[-1] for box_element in box_elements[:15]]
                        time.sleep(1)
                    if ultimas_tres_cores_1 != sequencia:

                        recent_results_element = driver.find_element(
                            By.ID, "roulette-recent")
                        box_elements = recent_results_element.find_elements(
                            By.CLASS_NAME, "sm-box")
                        sequencia_2 = [box_element.get_attribute(
                            "class").split()[-1] for box_element in box_elements[:15]]
                        ultimas_tres_cores_2 = sequencia_2[:3]


                        # Verifica se as duas sequências são iguais
                        if ultimas_tres_cores_1 != sequencia_anterior[:3]:
                            print("Acerto direto !!")
                            acertos_direto += 1
                        else:
                            if ultimas_tres_cores_1 != ultimas_tres_cores_2:
                                print("Acerto gale !!")
                                acertos_gale += 1
                            else:
                                print("Erro gale !!")
                                erros += 3

                        print(f"Acertos direto: {acertos_direto}, Acertos gale: {
                              acertos_gale}, Erros: {erros}")

                # Define alarme_acionado como False após coletar a segunda sequência
                alarme_acionado = False
                time.sleep(1)

    except Exception as e:
        error_message = f"Erro: {e}"
        print(error_message)

    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
