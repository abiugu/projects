import os
import pandas as pd

# Função para ler as listas de jogadas e quantidades de arquivos diferentes
def ler_listas(caminho_arquivo1, caminho_arquivo2):
    with open(caminho_arquivo1, 'r') as arquivo1, open(caminho_arquivo2, 'r') as arquivo2:
        lista1 = [linha.strip() for linha in arquivo1.readlines()]
        lista2 = [linha.strip() for linha in arquivo2.readlines()]
    return lista1, lista2

# Função para criar a planilha de comparação das jogadas
def criar_planilha(lista1, lista2):
    # Cria um dicionário para armazenar as jogadas e suas quantidades
    jogadas = {}

    # Adiciona as jogadas e suas quantidades da primeira lista ao dicionário
    for i in range(len(lista1)):
        if lista1[i].startswith("Ultimos"):
            chave = lista1[i]
            valor = int(lista1[i+2].split(': ')[1])
            if chave in jogadas:
                jogadas[chave] += valor
            else:
                jogadas[chave] = valor

    # Adiciona as jogadas e suas quantidades da segunda lista ao dicionário
    for i in range(len(lista2)):
        if lista2[i].startswith("Ultimos"):
            chave = lista2[i]
            valor = int(lista2[i+2].split(': ')[1])
            if chave in jogadas:
                jogadas[chave] += valor
            else:
                jogadas[chave] = valor

    # Cria um DataFrame a partir do dicionário de jogadas
    df = pd.DataFrame(jogadas.items(), columns=['Sequencia', 'Quantidade'])
    df = df.sort_values(by='Quantidade', ascending=False)

    return df

# Função para salvar a planilha em um arquivo Excel
def salvar_planilha(df, caminho_saida):
    df.to_excel(caminho_saida, index=False)

# Caminhos dos arquivos de entrada e saída
pasta_logs = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS")
caminho_arquivo1 = os.path.join(pasta_logs, 'resultados_log_48.txt')
caminho_arquivo2 = os.path.join(pasta_logs, 'resultados_erros_log_48.txt')
caminho_saida = os.path.join(pasta_logs, 'planilha_percentual_erros.xlsx')

# Lê as listas de jogadas
lista1, lista2 = ler_listas(caminho_arquivo1, caminho_arquivo2)

# Cria a planilha de comparação das jogadas
df = criar_planilha(lista1, lista2)

# Salva a planilha em um arquivo Excel
salvar_planilha(df, caminho_saida)

print("Planilha de comparação das jogadas criada com sucesso!")
