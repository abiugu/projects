import os

# Função para ler o conteúdo de um arquivo de texto e somar os maiores valores de acertos diretos e gales
def somar_maiores_valores(arquivo):
    with open(arquivo, 'r') as f:
        linhas = f.readlines()

    acertos_diretos_total = 0
    acertos_gale_total = 0
    maior_acertos_diretos = 0
    maior_acertos_gale = 0

    for linha in linhas:
        if "Acertos direto: 0" in linha:
            acertos_diretos_total += maior_acertos_diretos
            maior_acertos_diretos = 0
        elif "Acertos gale: 0" in linha:
            acertos_gale_total += maior_acertos_gale
            maior_acertos_gale = 0
        else:
            partes = linha.split(",")
            for parte in partes:
                if "Acertos direto:" in parte:
                    acertos_d = int(parte.split(":")[1].strip())
                    if acertos_d > maior_acertos_diretos:
                        maior_acertos_diretos = acertos_d
                elif "Acertos gale:" in parte:
                    acertos_g = int(parte.split(":")[1].strip())
                    if acertos_g > maior_acertos_gale:
                        maior_acertos_gale = acertos_g

    return acertos_diretos_total, acertos_gale_total

# Diretório onde os arquivos serão lidos e o arquivo de saída será salvo
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
logs_path = os.path.join(desktop_path, 'LOGS')
arquivo_entrada = os.path.join(logs_path, 'log 48.txt')
arquivo_saida = os.path.join(logs_path, 'acertos.txt')

# Somar os maiores valores de acertos diretos e gales
acertos_diretos, acertos_gale = somar_maiores_valores(arquivo_entrada)

# Salvar os valores de acertos diretos e gales no mesmo arquivo
with open(arquivo_saida, 'w') as f:
    f.write(f"Acertos diretos: {acertos_diretos}\n")
    f.write(f"Acertos gale: {acertos_gale}")

print("Valores salvos com sucesso em:")
print(f" - {arquivo_saida}")
