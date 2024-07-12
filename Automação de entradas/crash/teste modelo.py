import joblib
import pandas as pd
import os
from datetime import datetime

# Caminho do modelo treinado
model_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'LOGS', 'modelo.pkl')

# Carregar o modelo treinado
modelo = joblib.load(model_path)
print("Modelo carregado com sucesso.")

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

        # Determinar a previsão com base na média das probabilidades
        prob_media = probabilidade.mean()
        if prob_media >= 0.5:
            print(f"Baseado na sequência de multiplicadores inseridos, a próxima jogada será maior que 2.00x (Probabilidade média: {prob_media:.2%})")
        else:
            print(f"Baseado na sequência de multiplicadores inseridos, a próxima jogada será menor que 2.00x (Probabilidade média: {prob_media:.2%})")

    except Exception as e:
        print(f"Erro durante a previsão: {e}")

# Solicitar ao usuário os multiplicadores
multiplicadores = []
while True:
    multiplicador_input = input("Insira um multiplicador (digite 'q' para sair): ")
    if multiplicador_input.lower() == 'q':
        break
    try:
        multiplicador = float(multiplicador_input)
        multiplicadores.append(multiplicador)
    except ValueError:
        print("Por favor, insira um número válido.")

# Realizar a previsão para a próxima jogada
prever_proxima_jogada(multiplicadores, modelo)
