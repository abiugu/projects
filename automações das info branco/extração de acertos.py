import os

def ler_arquivo(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
    except UnicodeDecodeError:
        with open(caminho, 'r', encoding='latin-1') as arquivo:  # Tenta usar latin-1 se utf-8 falhar
            linhas = arquivo.readlines()
    return linhas


def escrever_arquivo(caminho, linhas):
    with open(caminho, 'w', encoding='utf-8') as arquivo:
        for linha in linhas:
            arquivo.write(linha)

def encontrar_acertos(jogadas, erros):
    acertos = []
    for jogada in jogadas:
        if jogada not in erros:
            acertos.append(jogada)
    return acertos

# Caminhos dos arquivos
caminho_jogadas = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS", "resultados", "resultados_log_60 branco.txt")
caminho_erros = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS", "resultados", "resultados_erros_log_60 branco.txt")
caminho_acertos = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS", "resultados", "acertos branco.txt")

# Ler os arquivos de jogadas e erros
jogadas = ler_arquivo(caminho_jogadas)
erros = ler_arquivo(caminho_erros)

# Encontrar os acertos
acertos = encontrar_acertos(jogadas, erros)

# Escrever os acertos em um novo arquivo
escrever_arquivo(caminho_acertos, acertos)

print("Acertos foram salvos em 'acertos.txt'.")
