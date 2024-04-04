import time
from alerta44 import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service()
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Executar em modo headless
# options.add_argument("--start-maximized")  # Maximizar a janela do navegador

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")


def verificar_stop():
    stop_path = os.path.join(desktop_path, "stop.txt")
    return os.path.exists(stop_path)


try:
    # Inicializa o driver do Selenium
    driver = webdriver.Chrome(service=service, options=options)  # ou webdriver.Firefox() se estiver usando o Firefox

    # Abre o site da Blaze
    driver.get("https://blaze1.space/pt/games/double?modal=auth&tab=login")

    # Preenche o campo de email com o valor fornecido
    campo_email = driver.find_element(By.NAME, 'username')
    campo_email.send_keys("abiugu@gmail.com")

    # Preenche o campo de senha com o valor fornecido
    campo_senha = driver.find_element(By.NAME, 'password')
    campo_senha.send_keys("Abiugu0203@")

    botao_entrar = driver.find_element(
        By.CSS_SELECTOR, 'button.red.submit.shared-button-custom')
    botao_entrar.click()

    print("Email e senha preenchidos com sucesso!")

    while True:
        # Verifica se o alarme está acionado
        if alarme_acionado:
            if cor_atual == 'red':
                condicao_vermelho = True
                print("sequencia vermelha")
            elif cor_atual == 'black':
                condicao_preto = True
                print("sequencia preta")

            # Encontra o campo de entrada de quantidade e define o valor como 0.10
            campo_quantidade = driver.find_element(
                By.CSS_SELECTOR, '.balance-input-field .input-field')
            driver.execute_script(
                "arguments[0].setAttribute('value', '0.50')", campo_quantidade)

            botao_comecar_jogo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.shared-button-custom.css-1apb7jj')))

            # Se a condição para preto for atendida, seleciona preto e branco
            if condicao_vermelho:

                # Seleciona a cor preta
                driver.find_element(
                    By.CSS_SELECTOR, '.input-wrapper.select .black').click()
                botao_comecar_jogo.click()

                # Seleciona também a cor branca
                driver.find_element(
                    By.CSS_SELECTOR, '.input-wrapper.select .white').click()
                campo_quantidade = driver.find_element(
                    By.CSS_SELECTOR, '.balance-input-field .input-field')
                driver.execute_script(
                    "arguments[0].setAttribute('value', '0.10')", campo_quantidade)
                botao_comecar_jogo.click()

            # Se a condição para vermelho for atendida, seleciona vermelho e branco
            elif condicao_preto:
                # Seleciona a cor vermelha
                driver.find_element(
                    By.CSS_SELECTOR, '.input-wrapper.select .red').click()
                botao_comecar_jogo.click()

                # Seleciona também a cor branca
                driver.find_element(
                    By.CSS_SELECTOR, '.input-wrapper.select .white').click()
                campo_quantidade = driver.find_element(
                    By.CSS_SELECTOR, '.balance-input-field .input-field')
                driver.execute_script(
                    "arguments[0].setAttribute('value', '0.10')", campo_quantidade)
                botao_comecar_jogo.click()

            print("Entrada direta configurada com sucesso!")
            cor_anterior = cor_atual

            time.sleep(30)

            # Utiliza a mesma cor da entrada direta na entrada da gale
            if cor_anterior == cor_atual:
                if cor_atual == 'red':
                    condicao_vermelho = True
                elif cor_atual == 'black':
                    condicao_preto = True

            # Encontra o campo de entrada de quantidade e define o valor como 0.10
                campo_quantidade = driver.find_element(
                    By.CSS_SELECTOR, '.balance-input-field .input-field')
                driver.execute_script(
                    "arguments[0].setAttribute('value', '0.50')", campo_quantidade)

                botao_comecar_jogo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button.shared-button-custom.css-1apb7jj')))

            # Se a condição para preto for atendida, seleciona preto e branco
                if condicao_vermelho:

                    # Seleciona a cor preta
                    driver.find_element(
                        By.CSS_SELECTOR, '.input-wrapper.select .black').click()
                    botao_comecar_jogo.click()

                # Seleciona também a cor branca
                    driver.find_element(
                        By.CSS_SELECTOR, '.input-wrapper.select .white').click()
                    campo_quantidade = driver.find_element(
                        By.CSS_SELECTOR, '.balance-input-field .input-field')
                    driver.execute_script(
                        "arguments[0].setAttribute('value', '0.10')", campo_quantidade)
                    botao_comecar_jogo.click()

            # Se a condição para vermelho for atendida, seleciona vermelho e branco
                elif condicao_preto:
                    # Seleciona a cor vermelha
                    driver.find_element(
                        By.CSS_SELECTOR, '.input-wrapper.select .red').click()
                    botao_comecar_jogo.click()

                # Seleciona também a cor branca
                    driver.find_element(
                        By.CSS_SELECTOR, '.input-wrapper.select .white').click()
                    campo_quantidade = driver.find_element(
                        By.CSS_SELECTOR, '.balance-input-field .input-field')
                    driver.execute_script(
                        "arguments[0].setAttribute('value', '0.10')", campo_quantidade)
                    botao_comecar_jogo.click()

            cor_anterior = cor_atual
            print("Entrada gale configurada com sucesso!")

        # Aguarda um segundo antes de verificar novamente
        time.sleep(1)

except Exception as e:
    print("Ocorreu um erro:", e)

finally:
    # Fecha o navegador após a execução do código
    driver.quit()
