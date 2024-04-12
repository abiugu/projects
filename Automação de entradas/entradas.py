import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Caminho para o desktop, pode ser usado para checar arquivos de parada
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")


def verificar_stop():
    stop_path = os.path.join(desktop_path, "stop.txt")
    return os.path.exists(stop_path)


service = Service()  # Adicione o caminho do executável do ChromeDriver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)

# Acessa o site
driver.get("https://blaze1.space/pt/games/double?modal=auth&tab=login")

# Login
campo_email = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'username')))
campo_email.send_keys("abiugu@gmail.com")
campo_senha = driver.find_element(By.NAME, 'password')
campo_senha.send_keys("Abiugu0203@")
botao_entrar = driver.find_element(
    By.CSS_SELECTOR, 'button.red.submit.shared-button-custom')
botao_entrar.click()
print("Email e senha preenchidos com sucesso!")

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "roulette-recent")))


def obter_ultimas_tres_cores():
    recent_results_element = driver.find_element(By.ID, "roulette-recent")
    box_elements = recent_results_element.find_elements(
        By.CLASS_NAME, "sm-box")
    sequencia = [box_element.get_attribute(
        "class").split()[-1] for box_element in box_elements[:15]]
    return sequencia[:3]


def obter_cor_oposta(cor_atual):
    return 'red' if cor_atual == 'black' else 'black'


sequencia_anterior = []
sequencia = obter_ultimas_tres_cores()

# Estratégia de aposta baseada em estatísticas
while True:
    if sequencia != sequencia_anterior:
        if len(set(sequencia[:3])) == 1:  # Se as três últimas cores são iguais
            cor_atual = sequencia[0]
            cor_oposta = obter_cor_oposta(cor_atual)

            # Coloque aqui a lógica para realizar a aposta
            print(f"Aposta de 0.50 na cor {cor_oposta} realizada com sucesso!")

        sequencia_anterior = sequencia.copy()
        time.sleep(10)  # Pequena pausa antes de verificar novamente
        sequencia = obter_ultimas_tres_cores()
    else:
        print("Aguardando mudança na sequência.")
        time.sleep(1)  # Checa a sequência a cada segundo até mudar


# Estratégia de aposta baseada em estatísticas
while sequencia == sequencia_anterior:
                        recent_results_element = driver.find_element(
                            By.ID, "roulette-recent")
                        box_elements = recent_results_element.find_elements(
                            By.CLASS_NAME, "sm-box")
                        sequencia = [box_element.get_attribute(
                            "class").split()[-1] for box_element in box_elements[:15]]

                        time.sleep(1)
    if len(set(sequencia[:3])) == 1:  # Se as três últimas cores são iguais
        cor_atual = sequencia[0]
        cor_oposta = obter_cor_oposta(cor_atual)
        percentuais_100 = extrair_percentuais(100)
        percentuais_25 = extrair_percentuais(25)
        percentuais_500 = extrair_percentuais(500)
        cor_atual_percentual_500 = int(
                            percentuais_500[['white', 'black', 'red'].index(cor_atual)])
        cor_oposta_percentual_500 = int(
            percentuais_500[['white', 'black', 'red'].index(cor_oposta)])
        cor_atual_percentual_100 = int(
            percentuais_100[['white', 'black', 'red'].index(cor_atual)])
        cor_oposta_percentual_100 = int(
            percentuais_100[['white', 'black', 'red'].index(cor_oposta)])
        cor_atual_percentual_25 = int(
            percentuais_25[['white', 'black', 'red'].index(cor_atual)])
        # Logica de decisão baseada nos percentuais extraídos
        if cor_atual_percentual_25 <= 48 and cor_atual_percentual_100 >= cor_oposta_percentual_100 and cor_atual_percentual_500 <= cor_oposta_percentual_500:
                print(f"Apostar na cor {cor_oposta} baseado nas estatísticas de percentuais")
                # Coloque aqui o código para realizar a aposta

    time.sleep(10)  # Pequena pausa antes de verificar novamente

    campo_quantidade = driver.find_element(By.CSS_SELECTOR, '.balance-input-field .input-field')
    driver.execute_script("arguments[0].setAttribute('value', '0.50')", campo_quantidade)

    botao_comecar_jogo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, f'button.shared-button-custom[data-bet="{obter_cor_oposta}"]')))
    botao_comecar_jogo.click()
    print(f"Aposta de 0.50 na cor {cor_oposta} realizada com sucesso!")
    valor_aposta_branco = 0.10
    driver.execute_script("arguments[0].setAttribute('value', '{}')".format(valor_aposta_branco), campo_quantidade)
    botao_apostar_branco = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button.shared-button-custom[data-bet="white"]')))
    botao_apostar_branco.click()
    print(f"Aposta adicional de 0.10 na cor branca realizada com sucesso!")

    time.sleep(20)  # Espera o resultado da rodada
    if obter_ultimas_tres_cores()[0] == cor_atual:
            novo_valor = 1.00  # Dobro do valor inicial
            driver.execute_script("arguments[0].setAttribute('value', '{}')".format(novo_valor), campo_quantidade)
            botao_comecar_jogo.click()
            print(f"Gale realizado com aposta de {novo_valor} na cor {obter_cor_oposta}!")

            valor_aposta_branco = 0.20
    driver.execute_script("arguments[0].setAttribute('value', '{}')".format(valor_aposta_branco), campo_quantidade)
    botao_apostar_branco = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button.shared-button-custom[data-bet="white"]')))
    botao_apostar_branco.click()
    print(f"Aposta adicional de 0.20 na cor branca realizada com sucesso!")

    time.sleep(10)  # Pequena pausa antes de verificar novamente
