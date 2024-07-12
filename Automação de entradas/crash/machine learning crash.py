import re
import os
import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Função para ler o arquivo de histórico local
def ler_arquivo(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
    return linhas

# Função para extrair dados da linha do histórico
def extrair_dados(linha):
    pattern = r'Multiplicador: ([\d\.]+,[\d]+) x - (\d{2}/\d{2}/\d{4}) \| (\d{2}:\d{2}:\d{2})'
    match = re.match(pattern, linha.strip())
    if match:
        try:
            multiplicador_str = match.group(1).replace('.', '').replace(',', '.')
            multiplicador = float(multiplicador_str)
            data = datetime.strptime(f"{match.group(2)} {match.group(3)}", '%d/%m/%Y %H:%M:%S')
            return multiplicador, data
        except ValueError:
            print(f"Erro ao converter multiplicador: {match.group(1)}")
            return None, None
    return None, None

# Função para extrair características das jogadas anteriores
def extrair_caracteristicas(dados):
    features = []
    for multiplicador, data in dados:
        if multiplicador is not None and data is not None:
            features.append({
                'Multiplicador': multiplicador,
                'Dia': data.day,
                'Mês': data.month,
                'Hora': data.hour,
                'Minuto': data.minute
            })
    
    return pd.DataFrame(features)

# Função para treinar o modelo de machine learning
def treinar_modelo(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo: {accuracy:.2f}")
    return clf

# Função principal para ler o arquivo, extrair características e treinar o modelo
def preparar_modelo(input_filepath):
    # Ler e processar o arquivo de histórico
    linhas = ler_arquivo(input_filepath)
    dados = [extrair_dados(linha) for linha in linhas]
    dados = [(m, d) for m, d in dados if m is not None and d is not None]
    
    # Extrair características das jogadas anteriores
    X = extrair_caracteristicas(dados)
    y = [1 if multiplicador > 2.00 else 0 for multiplicador, _ in dados]
    
    # Treinar o modelo de machine learning
    modelo = treinar_modelo(X, y)
    return modelo

# Diretório de entrada e nome do arquivo
input_dir = os.path.join(os.path.expanduser('~'), 'Desktop')
input_filename = 'resultados_bets.txt'
input_filepath = os.path.join(input_dir, input_filename)

# Preparar o modelo com base no arquivo de histórico
modelo = preparar_modelo(input_filepath)
print("Modelo treinado com sucesso.")

# Salvar o modelo
model_path = os.path.join(input_dir,"LOGS", 'modelo.pkl')
joblib.dump(modelo, model_path)
print(f"Modelo salvo em: {model_path}")
