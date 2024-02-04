import os
import time
import random

def ler_resultados_do_arquivo(caminho_arquivo):
    with open(caminho_arquivo, 'r') as file:
        linhas = file.readlines()

    resultados = []
    for linha in linhas:
        # Parse a linha para extrair o número e a cor
        resultado = {}
        partes = linha.strip().split(', ')
        for parte in partes:
            chave, valor = parte.split(': ')
            resultado[chave] = int(valor) if chave == 'Número' else valor
        resultados.append(resultado)

    return resultados

def simular_entrada():
    # Simule a escolha de número e cor
    numero_escolhido = random.randint(0, 14)
    cores_possiveis = ['red', 'black', 'white']
    cor_escolhida = random.choice(cores_possiveis)

    return {'Número': numero_escolhido, 'Cor': cor_escolhida}

def comparar_resultados(real, simulado):
    return real['Número'] == simulado['Número'] and real['Cor'] == simulado['Cor']

def analisar_e_simular(resultados):
    # Padrão desejado para simulação (ajuste conforme necessário)
    padrao_desejado = {'Número': 5, 'Cor': 'red'}

    acertos = 0
    erros = 0

    for resultado_real in resultados:
        # Analise aqui se o resultado_real atende ao padrão desejado
        if resultado_real == padrao_desejado:
            # Simular entrada
            entrada_simulada = simular_entrada()

            # Comparar resultados
            if comparar_resultados(resultado_real, entrada_simulada):
                acertos += 1
            else:
                erros += 1

    return acertos, erros

# Caminho completo do arquivo no desktop
caminho_arquivo = os.path.join(os.path.expanduser("~"), "Desktop", "resultados_recentes.txt")

while True:
    resultados = ler_resultados_do_arquivo(caminho_arquivo)
    acertos, erros = analisar_e_simular(resultados)

    print(f'Acertos: {acertos}, Erros: {erros}')

    # Aguarde 5 segundos antes de analisar novamente
    time.sleep(5)
