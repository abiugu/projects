import os
from collections import Counter

def ler_log(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    return linhas

def verificar_sequencias(linhas):
    quebras = []
    i = 0

    while i < len(linhas):
        if 'Ultimos 3 resultados:' in linhas[i]:
            resultados_atual = linhas[i].strip().split(': ')[1]
            if resultados_atual == 'black, black, black' or resultados_atual == 'red, red, red':
                j = i + 1
                while j < len(linhas):
                    if 'Ultimos 3 resultados:' in linhas[j]:
                        resultados_proximo = linhas[j].strip().split(': ')[1]
                        if resultados_proximo != resultados_atual:
                            if j + 1 < len(linhas):
                                linha_seguinte = linhas[j + 1].strip()
                                quebras.append(linha_seguinte)
                            break
                    j += 1
        i += 1

    return quebras

def contar_black_red(quebras):
    black_count = 0
    red_count = 0

    for quebra in quebras:
        if 'black' in quebra:
            black_count += 1
        if 'red' in quebra:
            red_count += 1

    return black_count, red_count

def main():
    caminho_arquivo = os.path.expanduser('~/Desktop/LOGS/log 100 direto modded.txt')
    linhas = ler_log(caminho_arquivo)
    quebras = verificar_sequencias(linhas)
    
    contador = Counter(quebras)
    top_10_quebras = contador.most_common(10)
    
    black_count, red_count = contar_black_red(quebras)

    with open(os.path.expanduser('~/Desktop/top_10_quebras.txt'), 'w') as arquivo_saida:
        arquivo_saida.write("Top 10 linhas mais repetidas após a quebra de sequência:\n")
        for linha, contagem in top_10_quebras:
            arquivo_saida.write(f"{linha}: {contagem} vezes\n")
        arquivo_saida.write(f"\nTotal de 'black': {black_count}\n")
        arquivo_saida.write(f"Total de 'red': {red_count}\n")
        print("Arquivo salvo com sucesso !!")

if __name__ == '__main__':
    main()
