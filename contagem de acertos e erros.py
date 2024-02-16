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
    acerto_direto = 0
    erro_direto = 0
    acertos_apos_erro = 0
    erros_apos_erro = 0
    erro_encontrado = False

    # Iterando pelas linhas do arquivo
    for linha in linhas:
        if "Acerto !!" in linha:
            acerto_direto += 1
        if "Erro !!" in linha:
            erro_direto += 1
            erro_encontrado = True
        elif erro_encontrado:
            if "Acerto no Martingale !!" in linha:
                acertos_apos_erro += 1
                erro_encontrado = False
            elif "Erro no Martingale !!" in linha:
                erros_apos_erro += 1
                erro_encontrado = False

    return acertos_apos_erro, erros_apos_erro, erro_direto, acerto_direto


# Chamando a função para contar os acertos e erros
acertos, erros, erro, acerto = contar_acertos_erros(file_path)

# Exibindo os resultados
print("Número de acertos diretos:", acerto)
print("Número de erros diretos:", erro)
print("Número de acertos no martingale após um erro:", acertos)
print("Número de erros no martingale após um erro:", erros)
