import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import joblib
import os

# Diretório de entrada
input_dir = os.path.join(os.path.expanduser('~'), 'Desktop')

# Carregar o modelo
model_path = os.path.join(input_dir,"LOGS", 'modelo.pkl')
modelo = joblib.load(model_path)
print("Modelo carregado com sucesso.")

# Função para buscar dados ao vivo do site
def buscar_dados_ao_vivo(url, modelo):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar todas as entradas de histórico
            entries = soup.find_all('div', class_='entries')

            # Verificar se temos exatamente 22 entradas
            if len(entries) == 22:
                # Preparar dados das últimas 22 jogadas
                ultimas_jogadas = []
                for entry in entries:
                    multiplicador_element = entry.find('div', class_='bet-amount')
                    if multiplicador_element:
                        multiplicador_text = multiplicador_element.text.strip()
                        # Extrair o multiplicador da string
                        multiplicador = float(multiplicador_text.split(' ')[0].replace(',', '.'))
                        ultimas_jogadas.append(multiplicador)
                
                # Previsões com base no modelo treinado
                X_novo = pd.DataFrame({
                    'Multiplicador': ultimas_jogadas,
                    'Dia': [datetime.now().day] * len(ultimas_jogadas),
                    'Mês': [datetime.now().month] * len(ultimas_jogadas),
                    'Hora': [datetime.now().hour] * len(ultimas_jogadas),
                    'Minuto': [datetime.now().minute] * len(ultimas_jogadas)
                })
                
                probabilidade = modelo.predict_proba(X_novo)[:, 1]
                for i, prob in enumerate(probabilidade):
                    if prob >= 0.5:
                        print(f"Próxima jogada: Mais de 2.00x (Probabilidade: {prob:.2%})")
                    else:
                        print(f"Próxima jogada: Menor que 2.00x (Probabilidade: {prob:.2%})")
            else:
                print(f"Não foram encontradas exatamente 22 entradas de histórico.")
        else:
            print(f"Erro ao acessar a URL: {response.status_code}")
    except Exception as e:
        print(f"Erro ao buscar dados ao vivo: {str(e)}")

# URL do site para buscar dados ao vivo
url = 'https://blaze1.space/pt/games/crash'

try:
    while True:
        # Buscar dados ao vivo e fazer previsões
        buscar_dados_ao_vivo(url, modelo)
        time.sleep(30)  # Espera 30 segundos antes de verificar novamente
except KeyboardInterrupt:
    print("\nPrograma interrompido pelo usuário.")
