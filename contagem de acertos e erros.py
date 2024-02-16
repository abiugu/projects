import os
import re

# Definindo o caminho do arquivo de texto no desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_name = "historico acertos e erros 16.02.txt"
file_path = os.path.join(desktop_path, file_name)


# Função para extrair a cor de uma linha
def extrair_cor(linha):
    cor_regex = re.compile(r"Cor atual: (\w+)")
    match = cor_regex.search(linha)
    if match:
        return match.group(1)
    return None


# Função para contar os acertos e erros no martingale após um erro
def contar_acertos_erros(file_path):
    with open(file_path, 'r') as file:
        linhas = file.readlines()

    # Inicializando contadores e listas de cores
    acerto_direto = 0
    erro_direto = 0
    acertos_apos_erro = 0
    erros_apos_erro = 0
    erro_encontrado = False
    cores_acertos_apos_erro = []
    cores_erros_apos_erro = []

    # Iterando pelas linhas do arquivo
    for linha in linhas:
        if "Acerto !!" in linha:
            acerto_direto += 1
        elif "Erro !!" in linha:
            erro_direto += 1
            erro_encontrado = True
            cor = extrair_cor(linha)
            if cor:
                cores_erros_apos_erro.append(cor)
        elif erro_encontrado:
            if "Acerto no Martingale !!" in linha:
                acertos_apos_erro += 1
                erro_encontrado = False
                cor = extrair_cor(linha)
                if cor:
                    cores_acertos_apos_erro.append(cor)
            elif "Erro no Martingale !!" in linha:
                erros_apos_erro += 1
                erro_encontrado = False
                cor = extrair_cor(linha)
                if cor:
                    cores_erros_apos_erro.append(cor)

    return acertos_apos_erro, erros_apos_erro, erro_direto, acerto_direto, cores_acertos_apos_erro, cores_erros_apos_erro


# Chamando a função para contar os acertos e erros
acertos, erros, erro, acerto, cores_acertos, cores_erros = contar_acertos_erros(
    file_path)

# Exibindo os resultados
print("Número de acertos diretos:", acerto, "cores:", ", ".join(cores_acertos))
print("Número de erros diretos:", erro, "cores:", ", ".join(cores_erros))
print("Número de acertos no martingale após um erro:", acertos)
print("Número de erros no martingale após um erro:", erros)
