import pandas as pd
import os

# Função para ler o conteúdo de um arquivo de texto e retornar como lista de dicionários
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
                lista.append({"Sequência": f'\'{sequencia}', "Quantidade": quantidade})
                i += 1
            else:
                print(f"Erro: Formato inválido na linha {i + 1} do arquivo {arquivo}.")
                return None
        elif linhas[i].startswith("Quantidade:"):
            # Se a linha for uma quantidade sem uma sequência correspondente, pule
            i += 1
        elif linhas[i].strip() == "":
            # Pular linhas em branco
            i += 1
        else:
            print(f"Erro: Formato inválido na linha {i + 1} do arquivo {arquivo}.")
            return None
        
    return lista

# Diretório onde os arquivos serão lidos e o arquivo de saída será salvo
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
logs_path = os.path.join(desktop_path, 'LOGS')

# Verificar se a pasta LOGS existe, se não existir, criar
if not os.path.exists(logs_path):
    os.makedirs(logs_path)

# Arquivos de jogadas e erros
arquivo_jogadas = os.path.join(logs_path, 'jogadas.txt')
arquivo_erros = os.path.join(logs_path, 'erros.txt')
arquivo_saida = os.path.join(logs_path, 'planilha_jogadas_erros.xlsx')

# Verificar se os arquivos existem
if not os.path.exists(arquivo_jogadas):
    print(f"Erro: O arquivo {arquivo_jogadas} não existe.")
    exit()
if not os.path.exists(arquivo_erros):
    print(f"Erro: O arquivo {arquivo_erros} não existe.")
    exit()

# Ler os dados dos arquivos
jogadas = ler_arquivo(arquivo_jogadas)
if jogadas is None:
    exit()
    
erros = ler_arquivo(arquivo_erros)
if erros is None:
    exit()

# Criar DataFrames
df_jogadas = pd.DataFrame(jogadas)
df_erros = pd.DataFrame(erros)

# Adicionar a coluna de erros totais ao DataFrame de jogadas (erro * 3)
df_jogadas["Erros Totais"] = df_jogadas["Sequência"].map(lambda x: df_erros.loc[df_erros["Sequência"] == x, "Quantidade"].sum() * 3)

# Adicionar a coluna de percentual de erro ao DataFrame de jogadas
df_jogadas["Percentual de Erro"] = (df_jogadas["Erros Totais"] / df_jogadas["Quantidade"]) * 100 / 100  # Dividir por 100

# Salvar o DataFrame em um arquivo Excel na pasta LOGS no desktop
file_path = os.path.join(logs_path, 'planilha_jogadas_erros.xlsx')
df_jogadas.to_excel(file_path, index=False)

print(f"Arquivo salvo com sucesso em: {arquivo_saida}")
