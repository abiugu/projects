import os
import sys

# Caminho do arquivo de resultados no desktop
caminho_resultados = os.path.join(os.path.expanduser(
    "~"), "Desktop", "resultado sequencias.txt")

# Redirecionar a saída para um arquivo
with open(caminho_resultados, 'w') as arquivo_resultados:
    # Redirecionar a saída padrão para o arquivo
    sys.stdout = arquivo_resultados

    # Caminho do arquivo
    caminho_arquivo = os.path.join(os.path.expanduser(
        "~"), "Desktop", "resultados double.txt")

    try:
        # Abre o arquivo em modo de leitura
        with open(caminho_arquivo, 'r') as arquivo:
            # Lê todas as linhas do arquivo
            linhas = arquivo.readlines()

            # Inicializa variáveis para contar sequências
            sequencias_encontradas_black = 0
            sequencias_encontradas_red = 0
            sequencia_atual_black = 0
            sequencia_atual_red = 0
            linhas_sequencias_encontradas = set()

            # Função para verificar e contar sequências
            def contar_sequencias(indice, cor, sequencias_encontradas):
                sequencia_atual = 0
                while (indice + sequencia_atual) < len(linhas) and cor in linhas[indice + sequencia_atual].lower():
                    sequencia_atual += 1
                if sequencia_atual >= 6:
                    sequencias_encontradas += 1
                    linhas_sequencias_encontradas.update(
                        range(indice, indice + sequencia_atual))
                    print(f"Sequência de {sequencia_atual} {
                          cor} consecutivos encontrada na linha {indice + 1}.")
                return sequencias_encontradas

            # Itera sobre as linhas do arquivo
            for indice, linha in enumerate(linhas):
                # Verifica se a linha já foi contada em alguma sequência anterior
                if indice in linhas_sequencias_encontradas:
                    continue

                # Verifica se há uma sequência de 'black' consecutivos
                sequencias_encontradas_black = contar_sequencias(
                    indice, 'black', sequencias_encontradas_black)

                # Verifica se há uma sequência de 'red' consecutivos
                sequencias_encontradas_red = contar_sequencias(
                    indice, 'red', sequencias_encontradas_red)

            # Imprime o total de sequências encontradas
            print(f"Total de sequências de black encontradas: {
                  sequencias_encontradas_black}")
            print(f"Total de sequências de red encontradas: {
                  sequencias_encontradas_red}")

    except FileNotFoundError:
        print(f"Arquivo {caminho_arquivo} não encontrado.")
    except Exception as e:
        print(f"Erro ao analisar resultados: {e}")
