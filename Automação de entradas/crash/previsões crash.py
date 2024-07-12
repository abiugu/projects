import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import joblib
import os

# Diretório onde o modelo está armazenado
input_dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'LOGS')

# Caminho do modelo treinado
model_path = os.path.join(input_dir, 'modelo.pkl')

# Carregar o modelo
modelo = joblib.load(model_path)
print("Modelo carregado com sucesso.")

# Configurar o webdriver do Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL do site para buscar dados ao vivo
url = 'https://blaze1.space/pt/games/crash?modal=crash_history_index'

# Variável para armazenar o último multiplicador processado
ultimo_multiplicador = None

def prever_proxima_jogada(multiplicadores, modelo):
    try:
        # Preparar dados para previsão
        X_teste = pd.DataFrame({
            'Multiplicador': multiplicadores,
            'Dia': [datetime.now().day] * len(multiplicadores),
            'Mês': [datetime.now().month] * len(multiplicadores),
            'Hora': [datetime.now().hour] * len(multiplicadores),
            'Minuto': [datetime.now().minute] * len(multiplicadores)
        })

        # Realizar previsão
        probabilidade = modelo.predict_proba(X_teste)[:, 1]

        # Determinar a previsão com base na sequência atual
        probabilidade_media = probabilidade.mean()
        previsao = "Mais de 2.00x" if probabilidade_media >= 0.5 else "Menor que 2.00x"

        return previsao, probabilidade_media

    except Exception as e:
        print(f"Erro durante a previsão: {e}")
        return None, None

def buscar_e_prever(url, modelo):
    global ultimo_multiplicador
    try:
        while True:
            # Navegar até a página inicial do histórico de apostas
            driver.get(url)

            # Aguardar o carregamento completo da página
            driver.implicitly_wait(10)  # Espera implícita de até 10 segundos

            # Encontrar todos os elementos de aposta 'bet' na página atual
            bet_elements = driver.find_elements(By.CSS_SELECTOR, 'div#history div.bet')

            # Lista para armazenar os multiplicadores desta página
            multiplicadores_pagina = []

            # Processar cada elemento de aposta para extrair o multiplicador
            for bet_element in bet_elements:
                try:
                    multiplier_element = bet_element.find_element(By.CSS_SELECTOR, 'div.bet-amount')
                    multiplier = float(multiplier_element.text.strip().replace('x', '').replace(',', '.'))
                    multiplicadores_pagina.append(multiplier)
                except Exception as e:
                    print(f"Erro ao extrair multiplicador: {e}")

            # Verificar se há novos multiplicadores nesta página
            if multiplicadores_pagina:
                # Obter o primeiro multiplicador (o mais recente)
                novo_multiplicador = multiplicadores_pagina[0]

                # Verificar se o multiplicador mudou desde a última iteração
                if novo_multiplicador != ultimo_multiplicador:
                    ultimo_multiplicador = novo_multiplicador

                    # Imprimir o último multiplicador processado (o mais recente)
                    print(f"\nÚltima jogada processada: {ultimo_multiplicador:.2f}")

                    # Previsão com base no modelo treinado e na sequência da página atual
                    resultado, probabilidade = prever_proxima_jogada(multiplicadores_pagina, modelo)

                    if resultado:
                        print(f"Próxima jogada: {resultado} (Probabilidade: {probabilidade:.2%})")

            # Esperar um curto período antes de verificar novamente
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
    except Exception as e:
        print(f"Erro ao buscar dados e prever: {str(e)}")
    finally:
        # Fechar o webdriver ao finalizar
        driver.quit()

# Iniciar a função para buscar dados e prever continuamente
try:
    buscar_e_prever(url, modelo)
except Exception as e:
    print(f"Erro durante a execução do script: {e}")
