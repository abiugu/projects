import os

# Definindo o caminho do arquivo de texto no desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_name = "historico acertos e erros 10.02.txt"
file_path = os.path.join(desktop_path, file_name)

# Função para contar os acertos e erros no martingale após um erro


def contar_acertos_erros(file_path):
    with open(file_path, 'r') as file:
        linhas = file.readlines()

    # Inicializando contadores
    acertos_apos_erro = 0
    erros_apos_erro = 0
    erro_encontrado = False

    # Iterando pelas linhas do arquivo
    for linha in linhas:
        if "Erro !!" in linha:
            erro_encontrado = True
        elif erro_encontrado:
            if "Acerto no Martingale !!" in linha:
                acertos_apos_erro += 1
                erro_encontrado = False
            elif "Erro no Martingale !!" in linha:
                erros_apos_erro += 1
                erro_encontrado = False

    return acertos_apos_erro, erros_apos_erro


# Chamando a função para contar os acertos e erros
acertos, erros = contar_acertos_erros(file_path)

# Exibindo os resultados
print("Número de acertos no martingale após um erro:", acertos)
print("Número de erros no martingale após um erro:", erros)
