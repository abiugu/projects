import os

# Função para identificar os alarmes e suas informações relevantes
def identificar_alarmes(arquivo):
    alarmes = []
    black_count = 0  # Contador para alarmes "black"
    red_count = 0   # Contador para alarmes "red"
    white_count = 0  # Contador para alarmes "white"
    with open(arquivo, 'r') as file:
        lines = file.readlines()  # Lê todas as linhas do arquivo
        for i, linha in enumerate(lines):
            if "Ultimos 3 resultados:" in linha:
                info = {}
                cores = linha.split(":")[1].strip().split(", ")
                cor_atual = cores[0]
                info["cor"] = cor_atual
            elif "Ultimas 25 porcentagens:" in linha:
                info["comp_25"] = [float(p)
                                   for p in linha.split(":")[1].split(", ")]
            elif "Ultimas 50 porcentagens:" in linha:
                info["comp_50"] = [float(p)
                                   for p in linha.split(":")[1].split(", ")]
            elif "Ultimas 100 porcentagens:" in linha:
                info["comp_100"] = [float(p)
                                    for p in linha.split(":")[1].split(", ")]
            elif "Ultimas 500 porcentagens:" in linha:
                info["comp_500"] = [float(p)
                                    for p in linha.split(":")[1].split(", ")]
            elif "Alarme acionado" in linha:
                if any("white" in line.lower() for line in lines[i+1:i+6]):  # Verifica se "white" aparece nas próximas 10 linhas
                    white_count += 1
                if info["cor"] == "black":
                    black_count += 1
                elif info["cor"] == "red":
                    red_count += 1
                info["alarme"] = int(linha.split(":")[1])
                alarmes.append(info.copy())

    return alarmes, black_count, red_count, white_count

# Diretório onde estão os arquivos
diretorio_logs = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS")

# Arquivo a ser lido
arquivo_entrada = os.path.join(diretorio_logs, "log 48.txt")
# Arquivo de saída
arquivo_saida = os.path.join(diretorio_logs, "brancos log 48.txt")

# Identificar alarmes e contar quantos black, quantos red e quantos white
alarmes, black_count, red_count, white_count = identificar_alarmes(arquivo_entrada)

# Função para imprimir os resultados e contar as ocorrências
def imprimir_resultados(alarmes, black_count, red_count, white_count):
    with open(arquivo_saida, 'w') as file:
        for info in alarmes:
            cor_atual = info["cor"]
            file.write("Ultimos 3 resultados: {}, {}, {}\n".format(
                cor_atual, cor_atual, cor_atual))
            file.write("Ultimas 25 porcentagens: {}\n".format(
                ", ".join(map(str, info["comp_25"]))))
            file.write("Ultimas 50 porcentagens: {}\n".format(
                ", ".join(map(str, info["comp_50"]))))
            file.write("Ultimas 100 porcentagens: {}\n".format(
                ", ".join(map(str, info["comp_100"]))))
            file.write("Ultimas 500 porcentagens: {}\n".format(
                ", ".join(map(str, info["comp_500"]))))
            file.write("Alarme acionado: {}\n".format(info["alarme"]))

        file.write("\nContagem:\n")
        file.write("Black: {}\n".format(black_count))
        file.write("Red: {}\n".format(red_count))
        file.write("White: {}\n".format(white_count))

# Imprimir resultados
imprimir_resultados(alarmes, black_count, red_count, white_count)
print("Informações extraídas com sucesso!")
