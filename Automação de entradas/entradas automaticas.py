from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass  # Para solicitar a senha de forma segura

# Configurando o serviço do Chrome
service = Service()

# Configurando as opções do Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Maximizar a janela do navegador

# Inicializando o driver do Chrome
driver = webdriver.Chrome(service=service, options=options)

# Função para fazer login
def login(email, senha):
    driver.get("https://blaze1.space/pt/games/double?modal=auth&tab=login")

    # Aguardar até que o campo de e-mail esteja presente
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    # Inserir e-mail
    email_input = driver.find_element(By.NAME, "username")
    email_input.clear()
    email_input.send_keys(email)

    # Inserir senha
    senha_input = driver.find_element(By.NAME, "password")
    senha_input.clear()
    senha_input.send_keys(senha)

    # Clicar no botão "Entrar"
    entrar_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
    entrar_button.click()

# Função para realizar a aposta
def realizar_aposta(cor_oposta):
    # Aguardar até que o campo de valor de aposta esteja presente
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "input-field")))

    # Inserir valor da aposta
    valor_aposta_input = driver.find_element(By.CLASS_NAME, "input-field")
    valor_aposta_input.clear()
    valor_aposta_input.send_keys("10.00")

    # Selecionar a cor oposta
    if cor_oposta == 'black':
        cor_button = driver.find_element(By.XPATH, "//div[@class='black ']")
    elif cor_oposta == 'red':
        cor_button = driver.find_element(By.XPATH, "//div[@class='red ']")
    
    cor_button.click()

    # Clicar no botão "Começar o jogo"
    apostar_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Começar o jogo')]")
    
    # Aguardar até que o botão esteja clicável
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(apostar_button))
    apostar_button.click()

# Função principal
def main():
    email = "abiugu@gmail.com"
    senha = getpass.getpass("Digite sua senha: ")  # Solicitar senha ao usuário

    login(email, senha)
    
    # Simulação da sequência atual
    # Em um cenário real, você obteria essa informação a partir do outro código
    sequencia_atual = 'red'
    cor_oposta = 'black' if sequencia_atual == 'red' else 'red'

    realizar_aposta(cor_oposta)
    time.sleep(10)  # Aguardar para visualização do resultado

    driver.quit()

if __name__ == "__main__":
    main()
