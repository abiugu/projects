from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurando o serviço do Chrome
chrome_service = Service()  # Substitua pelo caminho do seu chromedriver

# Configurando as opções do Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Executar em modo headless (sem interface gráfica)

# Inicializando o driver do Chrome
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Abrindo a página de login
driver.get("https://blaze1.space/pt/games/double?modal=auth&tab=login")

# Aguarda o login manual e a mudança de URL para a página do jogo
while "?modal=auth&tab=login" in driver.current_url:
    time.sleep(1)

print("Login realizado com sucesso. Iniciando monitoramento de apostas...")

try:
    while True:
        try:
            # Acessa a página principal do jogo para monitorar a cor da última jogada
            driver.get("https://blaze1.space/pt/games/double")

            # Aguardando até que o elemento da última jogada esteja presente na página
            last_play_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".entries.main .entry .roulette-tile .sm-box"))
            )

            # Obtendo a cor da última jogada
            class_attribute = last_play_element.get_attribute("class")

            # Verificando a cor baseada na classe
            if "red" in class_attribute:
                cor_ultima_jogada = "red"
            elif "black" in class_attribute:
                cor_ultima_jogada = "black"
            elif "white" in class_attribute:
                cor_ultima_jogada = "white"
            else:
                cor_ultima_jogada = "cor não reconhecida"

            print(f"Última jogada foi {cor_ultima_jogada}")

            if cor_ultima_jogada in ["red", "black"]:
                # Escolher a cor oposta à última jogada
                cor_oposta = "black" if cor_ultima_jogada == "red" else "red"
                cor_oposta_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"div.{cor_oposta}"))
                )
                cor_oposta_button.click()

                # Inserir o valor no campo de Quantia
                valor_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.input-field-wrapper input.input-field"))
                )
                driver.execute_script("arguments[0].setAttribute('value', '1.00');", valor_field)

                # Tentar clicar no botão "Começar o jogo"
                comecar_jogo_button = None
                while not comecar_jogo_button:
                    try:
                        comecar_jogo_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.place-bet button:not([disabled])"))
                        )
                        comecar_jogo_button.click()
                    except Exception as e:
                        print(f"Erro ao tentar clicar no botão 'Começar o jogo': {e}")
                        time.sleep(5)  # Esperar 5 segundos antes de tentar novamente

                print("Aposta realizada. Aguardando próxima rodada...")

                # Aguardar 60 segundos após clicar no botão de aposta
                time.sleep(60)

            else:
                print("Aguardando próxima rodada para decidir a aposta.")

        except Exception as e:
            print(f"Erro ao tentar realizar a entrada: {e}")

        # Aguardar um tempo antes de verificar novamente
        time.sleep(10)  # Aguarda 10 segundos antes de verificar novamente

except KeyboardInterrupt:
    print("\nPrograma encerrado pelo usuário.")

finally:
    # Manter o navegador aberto para verificação manual
    print("Manter o navegador aberto para verificação manual.")
    while True:
        pass
