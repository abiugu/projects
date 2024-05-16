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

def encontrar_acertos(jogadas, erros, tamanho_bloco=9):  # Tamanho do bloco padrão de 9 linhas por jogada
    acertos = []
    i = 0
    while i < len(jogadas):
        bloco_jogadas = jogadas[i:i+tamanho_bloco]
        bloco_encontrado = False
        for j in range(0, len(erros)-tamanho_bloco+1, tamanho_bloco):
            if erros[j:j+tamanho_bloco] == bloco_jogadas:
                bloco_encontrado = True
                break
        if not bloco_encontrado:
            acertos.extend(bloco_jogadas)
        i += tamanho_bloco
    return acertos

# Caminhos dos arquivos
pasta_desktop = os.path.join(os.path.expanduser("~"), "Desktop")
caminho_jogadas = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS", "resultados", "resultados_log_60 branco.txt")
caminho_erros = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS", "resultados", "resultados_erros_log_60 branco.txt")
caminho_acertos = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS", "resultados", "resultados_acertos 60 branco.txt")

# Ler os arquivos de jogadas e erros
jogadas = ler_arquivo(caminho_jogadas)
erros = ler_arquivo(caminho_erros)

# Encontrar os acertos
acertos = encontrar_acertos(jogadas, erros)

# Escrever os acertos em um novo arquivo
escrever_arquivo(caminho_jogadas, acertos)

print("Acertos foram salvos em 'resultados_acertos branco.txt'.")
