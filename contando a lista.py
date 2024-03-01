import os

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
log_file_path = os.path.join(desktop_path, "historico_do_dia.txt")

# Função para ler o arquivo
def ler_arquivo():
    with open(log_file_path, "r") as file:
        linhas = file.readlines()
    return linhas

# Função para extrair as informações das listas detalhadas
def extrair_info(linhas):
    numeros_faltando = []
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()
        if linha.startswith('('):
            resultado_detalhado = linhas[i:i+15]
            numeros_presentes = [int(resultado.split(")")[0][1:]) for resultado in resultado_detalhado if resultado.startswith('(')]
            numeros_faltantes = [j for j in range(15) if j not in numeros_presentes]
            numeros_faltando.extend(numeros_faltantes)
            # Avança para a próxima linha após a lista
            i += 15
            while i < len(linhas) and not linhas[i].strip().startswith('('):
                i += 1
        else:
            i += 1
    return numeros_faltando

# Função para encontrar os padrões mais vistos
def encontrar_padrao_mais_visto(numeros_faltando):
    contador_unico = {}
    contador_dois = {}
    contador_tres = {}

    # Contagem dos números únicos menos vistos
    for numero in numeros_faltando:
        if numero in contador_unico:
            contador_unico[numero] += 1
        else:
            contador_unico[numero] = 1

    # Contagem das sequências de dois números menos vistos
    for i in range(len(numeros_faltando) - 1):
        sequencia_dois = (numeros_faltando[i], numeros_faltando[i+1])
        if sequencia_dois in contador_dois:
            contador_dois[sequencia_dois] += 1
        else:
            contador_dois[sequencia_dois] = 1
    
    # Contagem das sequências de três números menos vistos
    for i in range(len(numeros_faltando) - 2):
        sequencia_tres = (numeros_faltando[i], numeros_faltando[i+1], numeros_faltando[i+2])
        if sequencia_tres in contador_tres:
            contador_tres[sequencia_tres] += 1
        else:
            contador_tres[sequencia_tres] = 1

    # Encontrar o número único menos visto
    numero_unico_mais_visto = max(contador_unico, key=contador_unico.get)
    total_ocorrencias_unico = contador_unico[numero_unico_mais_visto]

    # Encontrar a sequência de dois números menos vistos
    sequencia_dois_mais_vista = max(contador_dois, key=contador_dois.get)
    total_ocorrencias_dois = contador_dois[sequencia_dois_mais_vista]

    # Encontrar a sequência de três números menos vistos
    sequencia_tres_mais_vista = max(contador_tres, key=contador_tres.get)
    total_ocorrencias_tres = contador_tres[sequencia_tres_mais_vista]

    return numero_unico_mais_visto, total_ocorrencias_unico, sequencia_dois_mais_vista, total_ocorrencias_dois, sequencia_tres_mais_vista, total_ocorrencias_tres

# Função para calcular os acertos e erros com as porcentagens da cor oposta e da cor atual
def calcular_acertos_erros(linhas):
    acertos = 0
    acertos_martingale = 0
    acertos_oposta = 0
    acertos_martingale_oposta = 0
    erros_martingale_42ouMenos_oposta = 0
    erros_martingale_maisDe42_oposta = 0
    erros_martingale_42ouMenos_mesmaCor = 0
    erros_martingale_maisDe42_mesmaCor = 0
    total_acertos = 0
    total_acertos_martingale = 0
    total_erros_martingale = 0

    index = 0
    while index < len(linhas):
        line = linhas[index].strip()
        if "Acerto !! Cor atual:" in line:
            total_acertos += 1
            cor_atual = line.split(":")[-1].strip()
            index += 1
            porcentagens = linhas[index].split("Ultimas 25 rodadas:")[-1].replace("[", "").replace("]", "").split(", ")
            porcentagem_cor_atual = porcentagens[["white", "black", "red"].index(cor_atual)].replace("%", "").strip()
            if porcentagem_cor_atual:
                porcentagem_cor_atual = int(''.join(filter(str.isdigit, porcentagem_cor_atual)))
                if porcentagem_cor_atual <= 52:
                    acertos += 1
                if porcentagem_cor_atual <= 42:
                    acertos_oposta += 1
        elif "Acerto no Martingale !! Cor atual:" in line:
            total_acertos_martingale += 1
            cor_atual = line.split(":")[-1].strip()
            index += 1
            porcentagens = linhas[index].split("Ultimas 25 rodadas:")[-1].replace("[", "").replace("]", "").split(", ")
            porcentagem_cor_atual = porcentagens[["white", "black", "red"].index(cor_atual)].replace("%", "").strip()
            if porcentagem_cor_atual:
                porcentagem_cor_atual = int(''.join(filter(str.isdigit, porcentagem_cor_atual)))
                if porcentagem_cor_atual <= 52:
                    acertos_martingale += 1
                if porcentagem_cor_atual <= 42:
                    acertos_martingale_oposta += 1
        elif "Erro no Martingale !! Cor atual:" in line:
            total_erros_martingale += 1
            cor_atual = line.split(":")[-1].strip()
            index += 1
            porcentagens = linhas[index].split("Ultimas 25 rodadas:")[-1].replace("[", "").replace("]", "").split(", ")
            porcentagem_cor_atual = porcentagens[["white", "black", "red"].index(cor_atual)].replace("%", "").strip()
            if porcentagem_cor_atual:
                porcentagem_cor_atual = int(''.join(filter(str.isdigit, porcentagem_cor_atual)))
                cor_oposta = {"black": "red", "red": "black"}[cor_atual]
                porcentagem_cor_oposta = porcentagens[["white", "black", "red"].index(cor_oposta)].replace("%", "").strip()
                if porcentagem_cor_oposta:
                    porcentagem_cor_oposta = int(''.join(filter(str.isdigit, porcentagem_cor_oposta)))
                    if porcentagem_cor_oposta <= 42:
                        erros_martingale_42ouMenos_oposta += 1
                    else:
                        erros_martingale_maisDe42_oposta += 1
                if porcentagem_cor_atual <= 42:
                    erros_martingale_42ouMenos_mesmaCor += 1
                else:
                    erros_martingale_maisDe42_mesmaCor += 1
        index += 1

    # Calcula a porcentagem de cada categoria em relação ao total de sua respectiva categoria
    porcentagem_acertos = (acertos / total_acertos) * 100 if total_acertos else 0
    porcentagem_acertos_martingale = (acertos_martingale / total_acertos_martingale) * 100 if total_acertos_martingale else 0
    porcentagem_acertos_oposta = (acertos_oposta / total_acertos) * 100 if total_acertos else 0
    porcentagem_acertos_martingale_oposta = (acertos_martingale_oposta / total_acertos_martingale) * 100 if total_acertos_martingale else 0
    porcentagem_erros_martingale_52ouMenos_oposta = (erros_martingale_42ouMenos_oposta / total_erros_martingale) * 100 if total_erros_martingale else 0
    porcentagem_erros_martingale_maisDe52_oposta = (erros_martingale_maisDe42_oposta / total_erros_martingale) * 100 if total_erros_martingale else 0
    porcentagem_erros_martingale_52ouMenos_mesmaCor = (erros_martingale_42ouMenos_mesmaCor / total_erros_martingale) * 100 if total_erros_martingale else 0
    porcentagem_erros_martingale_maisDe52_mesmaCor = (erros_martingale_maisDe42_mesmaCor / total_erros_martingale) * 100 if total_erros_martingale else 0

    return (acertos, total_acertos, round(porcentagem_acertos, 2)), (acertos_martingale, total_acertos_martingale, round(porcentagem_acertos_martingale, 2)), (acertos_oposta, total_acertos, round(porcentagem_acertos_oposta, 2)), (acertos_martingale_oposta, total_acertos_martingale, round(porcentagem_acertos_martingale_oposta, 2)), (erros_martingale_42ouMenos_oposta, total_erros_martingale, round(porcentagem_erros_martingale_52ouMenos_oposta, 2)), (erros_martingale_maisDe42_oposta, total_erros_martingale, round(porcentagem_erros_martingale_maisDe52_oposta, 2)), (erros_martingale_42ouMenos_mesmaCor, total_erros_martingale, round(porcentagem_erros_martingale_52ouMenos_mesmaCor, 2)), (erros_martingale_maisDe42_mesmaCor, total_erros_martingale, round(porcentagem_erros_martingale_maisDe52_mesmaCor, 2))

# Função principal
def main():
    linhas = ler_arquivo()
    numeros_faltando = extrair_info(linhas)
    acertos, acertos_martingale, acertos_oposta, acertos_martingale_oposta, erros_martingale_42ouMenos_oposta, erros_martingale_maisDe42_oposta, erros_martingale_42ouMenos_mesmaCor, erros_martingale_maisDe42_mesmaCor = calcular_acertos_erros(linhas)
    print("Acertos com 52% ou menos:", acertos[0], "(total", acertos[1], ") -", acertos[2], "%")
    print("Acertos Martingale com 52% ou menos:", acertos_martingale[0], "(total", acertos_martingale[1], ") -", acertos_martingale[2], "%")
    print("Acertos com 42% ou menos da cor oposta:", acertos_oposta[0], "(total", acertos_oposta[1], ") -", acertos_oposta[2], "%")
    print("Acertos Martingale com 42% ou menos da cor oposta:", acertos_martingale_oposta[0], "(total", acertos_martingale_oposta[1], ") -", acertos_martingale_oposta[2], "%")
    print("Erros Martingale com 42% ou menos da cor oposta:", erros_martingale_42ouMenos_oposta[0], "(total", erros_martingale_42ouMenos_oposta[1], ") -", erros_martingale_42ouMenos_oposta[2], "%")
    print("Erros Martingale com mais de 42% da cor oposta:", erros_martingale_maisDe42_oposta[0], "(total", erros_martingale_maisDe42_oposta[1], ") -", erros_martingale_maisDe42_oposta[2], "%")
    print("Erros Martingale com 42% ou menos da mesma cor:", erros_martingale_42ouMenos_mesmaCor[0], "(total", erros_martingale_42ouMenos_mesmaCor[1], ") -", erros_martingale_42ouMenos_mesmaCor[2], "%")
    print("Erros Martingale com mais de 42% da mesma cor:", erros_martingale_maisDe42_mesmaCor[0], "(total", erros_martingale_maisDe42_mesmaCor[1], ") -", erros_martingale_maisDe42_mesmaCor[2], "%")

    numero_unico_mais_visto, total_ocorrencias_unico, sequencia_dois_mais_vista, total_ocorrencias_dois, sequencia_tres_mais_vista, total_ocorrencias_tres = encontrar_padrao_mais_visto(numeros_faltando)
    print("\nNúmero único menos visto:", numero_unico_mais_visto, "- Total de ocorrências:", total_ocorrencias_unico)
    print("Sequência de dois números menos vistos:", sequencia_dois_mais_vista, "- Total de ocorrências:", total_ocorrencias_dois)
    print("Sequência de três números menos vistos:", sequencia_tres_mais_vista, "- Total de ocorrências:", total_ocorrencias_tres)

if __name__ == "__main__":
    main()
