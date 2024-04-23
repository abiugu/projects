import os

# Função para comparar a cor atual com a cor oposta
def comparar_porcentagens(cor_atual, cor_oposta, porcentagens_atual, porcentagens_oposta):
    if cor_atual == "red":
        if porcentagens_atual > porcentagens_oposta:
            return ">"
        elif porcentagens_atual < porcentagens_oposta:
            return "<"
        else:
            return "="
    elif cor_atual == "black":
        if porcentagens_atual > porcentagens_oposta:
            return "<"
        elif porcentagens_atual < porcentagens_oposta:
            return ">"
        else:
            return "="

# Função para identificar os alarmes e suas informações relevantes
def identificar_alarmes(arquivo):
    alarmes = []
    black_count = 0  # Contador para alarmes "black"
    red_count = 0   # Contador para alarmes "red"
    with open(arquivo, 'r') as file:
        info = {}
        for linha in file:
            if "Ultimos 3 resultados:" in linha:
                cores = linha.split(":")[1].strip().split(", ")
                cor_atual = cores[0]
                info["cor"] = cor_atual
            elif "Ultimas 25 porcentagens:" in linha:
                info["comp_25"] = [float(p) for p in linha.split(":")[1].split(", ")]
            elif "Ultimas 50 porcentagens:" in linha:
                info["comp_50"] = [float(p) for p in linha.split(":")[1].split(", ")]
            elif "Ultimas 100 porcentagens:" in linha:
                info["comp_100"] = [float(p) for p in linha.split(":")[1].split(", ")]
            elif "Ultimas 500 porcentagens:" in linha:
                info["comp_500"] = [float(p) for p in linha.split(":")[1].split(", ")]
            elif "Alarme acionado. Contagem:" in linha:
                if info["cor"] == "black":
                    black_count += 1
                elif info["cor"] == "red":
                    red_count += 1
                info["alarme"] = int(linha.split(":")[1])
                alarmes.append(info.copy())
                info.clear()
    return alarmes, black_count, red_count

# Diretório onde estão os arquivos
diretorio_logs = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS")

# Arquivo a ser lido
arquivo_entrada = os.path.join(diretorio_logs, "erros log 48.txt")
# Arquivo de saída
arquivo_saida = os.path.join(diretorio_logs, "resultados_erros_log_48.txt")

# Identificar alarmes e contar quantos black e quantos red
alarmes, black_count, red_count = identificar_alarmes(arquivo_entrada)

# Função para imprimir os resultados e contar as ocorrências
def imprimir_resultados(alarmes, black_count, red_count):
    contagem = {"<": {"25": 0, "50": 0, "100": 0, "500": 0},
                "=": {"25": 0, "50": 0, "100": 0, "500": 0},
                ">": {"25": 0, "50": 0, "100": 0, "500": 0}}
    with open(arquivo_saida, 'w') as file:
        for info in alarmes:
            cor_atual = info["cor"]
            cor_oposta = "red" if cor_atual == "black" else "black"
            for rodadas in ["25", "50", "100", "500"]:
                comp = comparar_porcentagens(cor_atual, cor_oposta, info.get("comp_" + rodadas, [0, 0, 0])[1], info.get("comp_" + rodadas, [0, 0, 0])[2])
                contagem[comp][rodadas] += 1
                file.write("Percentual {} rodadas: {}\n".format(rodadas, comp))
            file.write("Cor: {}\nAlarme: {}\n\n".format(cor_atual, info["alarme"]))
        file.write("\nContagem:\n")
        file.write("Black: {}\n".format(black_count))
        file.write("Red: {}\n".format(red_count))
        for comparacao, valores in contagem.items():
            for rodadas, quantidade in valores.items():
                file.write("Percentual {} rodadas {}: {}\n".format(rodadas, comparacao, quantidade))

# Imprimir resultados
imprimir_resultados(alarmes, black_count, red_count)
