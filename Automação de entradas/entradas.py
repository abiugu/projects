import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    service = Service()
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    return webdriver.Chrome(service=service, options=options)

def login(driver):
    driver.get("https://blaze1.space/pt/games/double?modal=auth&tab=login")
    driver.find_element(By.NAME, 'username').send_keys("abiugu@gmail.com")
    driver.find_element(By.NAME, 'password').send_keys("Abiugu0203@")
    driver.find_element(By.CSS_SELECTOR, 'button.red.submit.shared-button-custom').click()
    print("Login efetuado com sucesso!")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "roulette-recent")))

def obter_ultimas_tres_cores(driver):
    recent_results_element = driver.find_element(By.ID, "roulette-recent")
    box_elements = recent_results_element.find_elements(By.CLASS_NAME, "sm-box")
    sequencia = [box_element.get_attribute("class").split()[-1] for box_element in box_elements[:3]]
    return sequencia

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
    driver = setup_driver()
    login(driver)
    
    sequencia_anterior = obter_ultimas_tres_cores(driver)
    
    try:
        while not os.path.exists(os.path.join(os.path.expanduser("~"), "Desktop", "stop.txt")):
            if sequencia_anterior[0] == obter_ultimas_tres_cores(driver)[0]:
                apostar(driver, obter_cor_oposta(sequencia_anterior[0]), 0.50)
                apostar(driver, 'white', 0.10)
                time.sleep(20)  # Espera o resultado da rodada

                if obter_ultimas_tres_cores(driver)[0] == sequencia_anterior[0]:
                    apostar(driver, obter_cor_oposta(sequencia_anterior[0]), 1.00)
                    apostar(driver, 'white', 0.20)
                    time.sleep(10)  # Pequena pausa antes de verificar novamente
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
