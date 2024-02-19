def calcular_resultado_sem_martingale(erro_direto, acerto_direto, erros_martingale, acertos_martingale):
    return acerto_direto - erro_direto


def calcular_resultado_com_martingale(erro_direto, acerto_direto, erros_martingale, acertos_martingale):
    return (acerto_direto + acertos_martingale) - (erros_martingale * 3)


def resultado (valor):
    return valor


def comparar_possibilidades():
    # Pedindo ao usuário para inserir os resultados
    acerto_direto = int(input("Insira o número de acertos diretos: "))
    erro_direto = int(input("Insira o número de erros diretos: "))
    acertos_martingale = int(input("Insira o número de acertos com martingale: "))
    erros_martingale = int(input("Insira o número de erros com martingale: "))

    # Calculando os resultados
    resultado_sem_martingale = calcular_resultado_sem_martingale(
        erro_direto, acerto_direto, erros_martingale, acertos_martingale)
    resultado_com_martingale = calcular_resultado_com_martingale(
        erro_direto, acerto_direto, erros_martingale, acertos_martingale)

    # Invertendo o sinal dos resultados
    resultado_sem_martingale_invertido = resultado(
        resultado_sem_martingale)
    resultado_com_martingale_invertido = resultado(
        resultado_com_martingale)

    # Exibindo as duas possibilidades
    print("Resultado sem martingale:", resultado_sem_martingale_invertido)
    print("Resultado com martingale:", resultado_com_martingale_invertido)

    # Determinando a mais eficiente
    if resultado_sem_martingale_invertido > resultado_com_martingale_invertido:
        return "Sem martingale é a mais eficiente"
    elif resultado_sem_martingale_invertido < resultado_com_martingale_invertido:
        return "Com martingale é a mais eficiente"
    else:
        return "Ambas as opções são equivalentes"


# Chamando a função para comparar as possibilidades
melhor_situacao = comparar_possibilidades()

# Exibindo o resultado da comparação
print("Resultado:", melhor_situacao)
