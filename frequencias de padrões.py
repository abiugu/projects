import os

def ler_lista_numeros():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    arquivo_path = os.path.join(desktop_path, 'resultados double.txt')
    with open(arquivo_path, "r") as arquivo:
        linhas = arquivo.readlines()
    lista_numeros = []
    for linha in linhas:
        numero = int(linha.strip().split(",")[0].split(":")[1].strip())
        lista_numeros.append(numero)
    return lista_numeros

def encontrar_padroes_mais_vistos(lista_numeros):
    padroes_tres = {}
    padroes_quatro = {}
    padroes_cinco = {}

    for i in range(len(lista_numeros) - 2):  # Sequência de 3
        sequencia_tres = tuple(lista_numeros[i:i+3])
        if sequencia_tres in padroes_tres:
            padroes_tres[sequencia_tres] += 1
        else:
            padroes_tres[sequencia_tres] = 1

    for i in range(len(lista_numeros) - 3):  # Sequência de 4
        sequencia_quatro = tuple(lista_numeros[i:i+4])
        if sequencia_quatro in padroes_quatro:
            padroes_quatro[sequencia_quatro] += 1
        else:
            padroes_quatro[sequencia_quatro] = 1

    for i in range(len(lista_numeros) - 4):  # Sequência de 5
        sequencia_cinco = tuple(lista_numeros[i:i+5])
        if sequencia_cinco in padroes_cinco:
            padroes_cinco[sequencia_cinco] += 1
        else:
            padroes_cinco[sequencia_cinco] = 1

    # Ordenar os padrões por frequência e retornar os 5 padrões mais vistos de cada sequência
    top_padroes_tres = sorted(padroes_tres.items(), key=lambda x: x[1], reverse=True)[:5]
    top_padroes_quatro = sorted(padroes_quatro.items(), key=lambda x: x[1], reverse=True)[:5]
    top_padroes_cinco = sorted(padroes_cinco.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return top_padroes_tres, top_padroes_quatro, top_padroes_cinco


def main():
    lista_numeros = ler_lista_numeros()
    top_padroes_tres, top_padroes_quatro, top_padroes_cinco = encontrar_padroes_mais_vistos(lista_numeros)

    print("Padrões mais vistos de sequência de 3 números:")
    for i, (padrao, frequencia) in enumerate(top_padroes_tres, start=1):
        print(f"Padrão {i}: {padrao} - Total de vezes que ocorre: {frequencia}")

    print("\nPadrões mais vistos de sequência de 4 números:")
    for i, (padrao, frequencia) in enumerate(top_padroes_quatro, start=1):
        print(f"Padrão {i}: {padrao} - Total de vezes que ocorre: {frequencia}")

    print("\nPadrões mais vistos de sequência de 5 números:")
    for i, (padrao, frequencia) in enumerate(top_padroes_cinco, start=1):
        print(f"Padrão {i}: {padrao} - Total de vezes que ocorre: {frequencia}")


if __name__ == "__main__":
    main()
