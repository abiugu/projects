import getpass
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from alerta1 import alarme_acionado

# Configuração do serviço do Chrome
chrome_service = Service()  # Substitua pelo caminho do seu chromedriver

# Configuração das opções do Chrome (modo headless)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar em modo headless (sem interface gráfica)

# Inicialização do driver do Chrome
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

def fazer_login(driver, email, senha):
    driver.get("https://blaze1.space/pt/games/double?modal=auth&tab=login")
    
    # Preencher e-mail
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username")))
    email_field.send_keys(email)
    
    # Preencher senha
    senha_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password")))
    senha_field.send_keys(senha)
    
    # Clicar no botão de login
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='login-btn']")))
    login_button.click()

# Perguntar a senha no terminal
senha = getpass.getpass(prompt="Digite sua senha: ")

# Realizar login
fazer_login(driver, "abiugu@gmail.com", senha)
try:
    # URL da página onde você realiza as apostas
    url = "https://blaze1.space/pt/?modal=auth&tab=login"

    # Função para aguardar o alarme sound 2 ser ativado
    def aguardar_alarme_sound2():
       if alarme_acionado:
    # Executa a lógica para fazer a aposta na cor oposta
    # Extrai a cor atual da sequência e faz a aposta
        cor_atual = 'red'  # Substitua pela lógica real para obter a cor atual
        valor_aposta = 10.00
        cor_oposta = 'black' if cor_atual == 'red' else 'red'
        fazer_aposta(valor_aposta, cor_oposta)

    # Função para inserir o valor da aposta e clicar no botão de apostar
    def fazer_aposta(valor_aposta, cor_oposta):
        # Navegar para a página
        driver.get(url)

        # Aguardar até que o campo de quantidade esteja visível
        input_quantia = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".input-field-wrapper .input-field"))
        )

        # Limpar o campo e inserir o valor da aposta
        input_quantia.clear()
        input_quantia.send_keys(str(valor_aposta))

        # Selecionar a cor oposta à cor atual
        # Aqui, você precisa substituir 'black' pela lógica correta para escolher a cor oposta
        if cor_oposta == 'red':
            botao_cor_oposta = driver.find_element(By.CSS_SELECTOR, ".red")
        elif cor_oposta == 'black':
            botao_cor_oposta = driver.find_element(By.CSS_SELECTOR, ".black")
        else:
            botao_cor_oposta = driver.find_element(By.CSS_SELECTOR, ".white")

        botao_cor_oposta.click()

        # Clicar no botão para começar o jogo (ou similar)
        botao_apostar = driver.find_element(By.CSS_SELECTOR, ".shared-button-custom")
        botao_apostar.click()

    # Simulação de aguardar o alarme sound 2 ser ativado
    alarme_acionado = aguardar_alarme_sound2()

    if alarme_acionado:
        # Simulação de obter a cor atual da sequência
        cor_atual = 'red'  # Substitua pela lógica real para obter a cor atual da sequência

        # Definir o valor da aposta
        valor_aposta = 10.00

        # Determinar a cor oposta à cor atual
        if cor_atual == 'red':
            cor_oposta = 'black'
        elif cor_atual == 'black':
            cor_oposta = 'red'
        else:
            cor_oposta = 'black'  # Substitua pela lógica real para determinar a cor oposta

        # Realizar a aposta com a cor oposta
        fazer_aposta(valor_aposta, cor_oposta)

finally:
    # Fechar o navegador ao finalizar
    driver.quit()
