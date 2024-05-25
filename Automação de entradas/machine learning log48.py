import os
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Função para ler o arquivo de log e extrair os dados
def ler_arquivo_log(file_path):
    with open(file_path, 'r') as file:
        linhas = file.readlines()
    
    dados = []
    for i, linha in enumerate(linhas):
        if "Alarme acionado" in linha:
            jogada = linhas[i+1]
            proxima_jogada = linhas[i+2]
            dados.append((jogada, proxima_jogada))
    
    return dados

# Função para pré-processamento dos dados
def preprocessar_dados(dados):
    novas_jogadas = []
    for jogada, proxima_jogada in dados:
        jogada_info = jogada.split(", ")
        proxima_jogada_info = proxima_jogada.split(", ")
        
        # Verificando se os dados estão completos
        if len(jogada_info) >= 3 and len(proxima_jogada_info) >= 1:
            ultimas_cores = jogada_info[1].split(": ")[1].split(", ")
            ultimas_porcentagens = [float(x.split(": ")[1]) for x in jogada_info[2:]]
            
            proxima_cor = proxima_jogada_info[0].split(": ")[1]
            
            novas_jogadas.append(ultimas_cores + ultimas_porcentagens + [proxima_cor])
    
    colunas = ['Ultima Cor 1', 'Ultima Cor 2', 'Ultima Cor 3',
               'Ultimas 25 Porcentagens 1', 'Ultimas 25 Porcentagens 2', 'Ultimas 25 Porcentagens 3',
               'Ultimas 50 Porcentagens 1', 'Ultimas 50 Porcentagens 2', 'Ultimas 50 Porcentagens 3',
               'Ultimas 100 Porcentagens 1', 'Ultimas 100 Porcentagens 2', 'Ultimas 100 Porcentagens 3',
               'Ultimas 500 Porcentagens 1', 'Ultimas 500 Porcentagens 2', 'Ultimas 500 Porcentagens 3',
               'Proxima Cor']
    
    df = pd.DataFrame(novas_jogadas, columns=colunas)
    
    return df

# Função para treinar o modelo e fazer previsões
def treinar_e_prever(df):
    X = df.drop('Proxima Cor', axis=1)
    y = df['Proxima Cor']
    
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)
    
    clf = DecisionTreeClassifier()
    clf.fit(X, y_encoded)
    
    # Previsão para a próxima jogada
    ultima_jogada = X.iloc[-1]
    proxima_cor_predita_encoded = clf.predict([ultima_jogada])[0]
    
    # Mapeando o número da cor de volta para a cor original
    proxima_cor_predita = encoder.inverse_transform([proxima_cor_predita_encoded])[0]
    
    return proxima_cor_predita

# Caminho do arquivo de log
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
LOGS = os.path.join(desktop, "LOGS")
file_path = os.path.join(LOGS, "log 48 direto.txt")

# Ler e preprocessar os dados
dados = ler_arquivo_log(file_path)
df = preprocessar_dados(dados)

# Treinar o modelo e fazer previsões
proxima_cor = treinar_e_prever(df)
print("Próxima cor prevista:", proxima_cor)
