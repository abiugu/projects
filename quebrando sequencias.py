import os
from collections import Counter

def ler_lista_cores():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    arquivo_path = os.path.join(desktop_path, 'resultados double.txt')
    with open(arquivo_path, "r") as arquivo:
        linhas = arquivo.readlines()
    lista_cores = []
    for linha in linhas:
        cor = linha.strip().split(",")[1].split(":")[1].strip()
        lista_cores.append(cor)
    return lista_cores

def encontrar_sequencias_cores(lista_cores):
    sequencias_cores = []
    for i in range(len(lista_cores) - 6):
        sequencia_cinco_cores = tuple(lista_cores[i:i+5])
        proxima_cor = lista_cores[i+5]
        if len(set(sequencia_cinco_cores)) == 1 and proxima_cor != sequencia_cinco_cores[0]:
            sequencia_anterior = tuple(lista_cores[i-3:i])
            sequencias_cores.append((sequencia_anterior, sequencia_cinco_cores))
    sequencias_cores_counter = Counter(sequencias_cores)
    top_5_sequencias_cores = sequencias_cores_counter.most_common(5)
    return top_5_sequencias_cores

def main():
    lista_cores = ler_lista_cores()
    top_5_sequencias_cores = encontrar_sequencias_cores(lista_cores)

    if top_5_sequencias_cores:
        print("As 5 sequências mais vistas de cinco cores iguais seguidas por uma quebra de cor:")
        for i, ((sequencia_anterior, sequencia_cinco_cores), frequencia) in enumerate(top_5_sequencias_cores, start=1):
            print(f"Sequência {i}: Frequência: {frequencia}")
            print("  Cores Anteriores:", sequencia_anterior)
            print("  Sequência de Cinco Cores Iguais:", sequencia_cinco_cores)
    else:
        print("Não foram encontradas sequências de cinco cores iguais seguidas por uma quebra de cor na lista.")

if __name__ == "__main__":
    main()
