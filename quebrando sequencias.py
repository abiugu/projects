import os

def ler_lista_cores():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    arquivo_path = os.path.join(desktop_path, 'resultados double.txt')
    with open(arquivo_path, "r") as arquivo:
        linhas = arquivo.readlines()
    lista_cores = []
    for linha in linhas:
        if 'Cor:' in linha:  
            cor = linha.strip().split("Cor:")[1].strip().split()[0].lower()  
            lista_cores.append(cor)
    return lista_cores

def encontrar_sequencia(lista_cores, sequencia_anterior, sequencia_seguinte):
    sequencias_contagem = {}
    for i in range(sequencia_seguinte, len(lista_cores) - sequencia_anterior):
        sequencia = tuple(lista_cores[i-sequencia_anterior:i] + lista_cores[i:i+sequencia_seguinte])
        sequencias_contagem[sequencia] = sequencias_contagem.get(sequencia, 0) + 1
    sequencias_mais_ocorridas = sorted(sequencias_contagem.items(), key=lambda x: x[1], reverse=True)
    return sequencias_mais_ocorridas

def main():
    lista_cores = ler_lista_cores()

    # Solicitar ao usuário o tamanho das sequências
    sequencia_anterior = int(input("Digite o tamanho da sequência anterior desejada: "))
    sequencia_seguinte = int(input("Digite o tamanho da sequência seguinte desejada: "))

    # Encontrar a sequência mais vista
    sequencias_mais_ocorridas = encontrar_sequencia(lista_cores, sequencia_anterior, sequencia_seguinte)

    if sequencias_mais_ocorridas:
        print(f"As sequências de tamanho {sequencia_anterior} antes e {sequencia_seguinte} após mais vistas são:")
        for i, (sequencia, ocorrencias) in enumerate(sequencias_mais_ocorridas[:5], start=1):
            print(f"Sequência {i}: {sequencia} - Ocorrências: {ocorrencias}")
    else:
        print("Nenhuma sequência encontrada com os critérios especificados.")

if __name__ == "__main__":
    main()
