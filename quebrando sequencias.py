import os


def calcular_porcentagem_acerto(acertos, quebras):
    return (acertos / quebras) * 100 if quebras > 0 else 0


# Caminho completo do arquivo .txt na área de trabalho
txt_file_path = os.path.join(os.path.expanduser(
    "~"), "Desktop", "resultados double.txt")
output_file_path = os.path.join(os.path.expanduser(
    "~"), "Desktop", "quebra_de_sequencias.txt")

# Variáveis para armazenar informações sobre a sequência atual
ultima_cor = None
acertos_por_tamanho = {}
erros_por_tamanho = {}
quebras_por_tamanho = {}
quebra_atual = []

with open(txt_file_path, "r") as txt_file:
    for linha in txt_file:
        # Extrair a cor da linha
        cor = linha.split(",")[1].split(":")[1].strip()

        # Verificar quebras na sequência
        if ultima_cor is not None and cor != ultima_cor:
            # Verificar se a próxima linha é a cor oposta à linha anterior
            proxima_linha = next(txt_file, None)
            if proxima_linha:
                proxima_cor = proxima_linha.split(",")[1].split(":")[1].strip()
                if proxima_cor != ultima_cor:
                    acertos_por_tamanho[len(quebra_atual)] = acertos_por_tamanho.get(
                        len(quebra_atual), 0) + 1
                else:
                    erros_por_tamanho[len(quebra_atual)] = erros_por_tamanho.get(
                        len(quebra_atual), 0) + 1

            # Atualizar o dicionário se a sequência atual for maior que 2
            if len(quebra_atual) >= 3:
                quebras_por_tamanho[len(quebra_atual)] = quebras_por_tamanho.get(
                    len(quebra_atual), 0) + 1

            # Reiniciar a sequência atual
            quebra_atual = []

        # Atualizar a última cor
        ultima_cor = cor
        quebra_atual.append(cor)

# Calcular percentual médio de acertos
total_acertos = sum(acertos_por_tamanho.values())
total_quebras = sum(quebras_por_tamanho.values())
percentual_medio_acerto = calcular_porcentagem_acerto(
    total_acertos, total_quebras)

# Escrever o resultado no arquivo
with open(output_file_path, "w") as output_file:
    # Imprimir o resultado em ordem crescente
    for tamanho in sorted(quebras_por_tamanho.keys()):
        quebras = quebras_por_tamanho[tamanho]
        acertos = acertos_por_tamanho.get(tamanho, 0)
        percentual_acerto_tamanho = calcular_porcentagem_acerto(
            acertos, quebras)
        output_file.write(f"Foram encontradas {quebras} quebras de sequência de {
                          tamanho} cores consecutivas. ({percentual_acerto_tamanho:.2f}% de acerto)\n")

print(f"O resultado foi salvo em {output_file_path}")
