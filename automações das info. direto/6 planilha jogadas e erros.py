import os
import pandas as pd

def ler_arquivo(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()

    lista = []
    i = 0
    while i < len(linhas):
        if linhas[i].startswith("Sequencia:"):
            sequencia = linhas[i].split(": ")[1].strip()
            i += 1
            if i < len(linhas) and linhas[i].startswith("Quantidade:"):
                quantidade = int(linhas[i].split(": ")[1].strip())
                lista.append({"Sequência": f'\'{sequencia}',
                             "Total de Jogadas": quantidade})
                i += 1
            else:
                print(f"Erro: Formato inválido na linha {i + 1} do arquivo {arquivo}.")
                i += 1
        elif linhas[i].startswith("Quantidade:"):
            i += 1
        elif linhas[i].strip() == "":
            i += 1
        else:
            print(f"Ignorando linha {i + 1} do arquivo {arquivo}.")
            i += 1

    return lista

# Diretório onde os arquivos serão lidos e o arquivo de saída será salvo
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
logs_path = os.path.join(desktop_path, 'LOGS')

# Verificar se a pasta LOGS existe, se não existir, criar
if not os.path.exists(logs_path):
    os.makedirs(logs_path)

# Arquivos de jogadas, erros e acertos
arquivo_jogadas = os.path.join(logs_path, "sequencias", 'sequencias 48 direto.txt')
arquivo_erros = os.path.join(logs_path, "sequencias", 'sequencias erros 48 direto.txt')
arquivo_acertos = os.path.join(logs_path, "sequencias", 'sequencias acertos 48 direto.txt')
arquivo_saida = os.path.join(logs_path, 'planilha acertos 48 direto.xlsx')

# Verificar se os arquivos existem
for arquivo in [arquivo_jogadas, arquivo_erros, arquivo_acertos]:
    if not os.path.exists(arquivo):
        print(f"Erro: O arquivo {arquivo} não existe.")
        exit()

# Ler os dados dos arquivos
jogadas = ler_arquivo(arquivo_jogadas)
if jogadas is None:
    exit()

erros = ler_arquivo(arquivo_erros)
if erros is None:
    exit()

acertos = ler_arquivo(arquivo_acertos)
if acertos is None:
    exit()

# Criar DataFrames
df_jogadas = pd.DataFrame(jogadas)
df_erros = pd.DataFrame(erros)
df_acertos = pd.DataFrame(acertos)

# Adicionar a coluna de erros totais ao DataFrame de jogadas (erro * 3)
df_jogadas["Erros Totais"] = df_jogadas["Sequência"].map(
    lambda x: df_erros.loc[df_erros["Sequência"] == x, "Total de Jogadas"].sum() if x in df_erros["Sequência"].values else 0)

# Adicionar a coluna de acertos totais ao DataFrame de jogadas
df_jogadas["Acertos Totais"] = df_jogadas["Sequência"].map(
    lambda x: df_acertos.loc[df_acertos["Sequência"] == x, "Total de Jogadas"].sum() if x in df_acertos["Sequência"].values else 0)

# Adicionar a coluna de percentual de acerto ao DataFrame de jogadas
df_jogadas["Percentual de Acerto"] = df_jogadas["Acertos Totais"] / df_jogadas["Total de Jogadas"]

# Selecionar apenas as colunas necessárias
df_jogadas = df_jogadas[["Sequência", "Total de Jogadas", "Erros Totais", "Acertos Totais", "Percentual de Acerto"]]

# Salvar o DataFrame em um arquivo Excel
df_jogadas.to_excel(arquivo_saida, index=False)

print(f"Arquivo salvo com sucesso em: {arquivo_saida}")
