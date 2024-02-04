from collections import Counter
import re
import os


def extrair_sequencias_cores(path):
    # Função para extrair sequências de cores de um arquivo de texto
    with open(path, 'r') as file:
        content = file.read()

    # Usando expressão regular para extrair sequências no formato "Número: Cor:"
    matches = re.findall(r'Número: \d+, Cor: (\w+)', content)

    # Criando uma lista de cores
    sequencias_cores = [cor for cor in matches]

    return sequencias_cores


def contar_sequencias_cores(sequencias_cores, comprimento_minimo=5):
    # Inicializando uma lista para armazenar sequências consecutivas
    sequencia_atual = []
    sequencias_consecutivas = []

    for cor in sequencias_cores:
        if len(sequencia_atual) == 0 or sequencia_atual[-1] != cor:
            sequencia_atual.append(cor)
        else:
            # Reiniciando a sequência se a cor não for diferente
            sequencia_atual = [cor]

        if len(sequencia_atual) >= comprimento_minimo:
            sequencias_consecutivas.append(tuple(sequencia_atual))

    # Contando as ocorrências de sequências consecutivas
    contagem_sequencias = Counter(sequencias_consecutivas)

    return contagem_sequencias


def escrever_resultados_filtrados_cores(contagem_sequencias, frequencia_minima=3, output_path=None):
    # Escrevendo as sequências consecutivas e suas contagens em ordem decrescente de frequência
    with open(output_path, 'w') as output_file:
        for sequencia, frequencia in contagem_sequencias.most_common():
            if frequencia >= frequencia_minima:
                output_file.write(
                    f'Sequência: {sequencia}, Frequência: {frequencia}\n')


# Caminho completo do arquivo .txt na área de trabalho
caminho_arquivo = os.path.join(os.path.expanduser(
    "~"), "Desktop", "resultados double.txt")
caminho_output = os.path.join(os.path.expanduser(
    "~"), "Desktop", "Frequências de padrões.txt")

sequencias_cores = extrair_sequencias_cores(caminho_arquivo)
contagem_sequencias_cores = contar_sequencias_cores(sequencias_cores)

# Escrevendo os resultados filtrados em um arquivo de texto no desktop
escrever_resultados_filtrados_cores(
    contagem_sequencias_cores, output_path=caminho_output)
