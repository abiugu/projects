def calcular_resultado_sem_martingale(erro_direto, acerto_direto, erros_martingale, acertos_martingale):
    return (erros_martingale + acertos_martingale) - acerto_direto

def calcular_resultado_com_martingale(erro_direto, acerto_direto, erros_martingale, acertos_martingale):
    return (erros_martingale * 3) - acerto_direto - acertos_martingale

def comparar_possibilidades():
    # Pedindo ao usuário para inserir os resultados
    acerto_direto = int(input("Insira o número de acertos diretos: "))
    acerto_direto = int(input("Insira o número de acertos diretos: "))
    acertos_martingale = int(input("Insira o número de acertos com martingale: "))
    erros_martingale = int(input("Insira o número de erros com martingale: "))

    # Calculando os resultados
    resultado_sem_martingale = calcular_resultado_sem_martingale(erro_direto, acerto_direto, erros_martingale, acertos_martingale)
    resultado_com_martingale = calcular_resultado_com_martingale(erro_direto, acerto_direto, erros_martingale, acertos_martingale)

    # Exibindo as duas possibilidades
    print("Resultado sem martingale:", resultado_sem_martingale)
    print("Resultado com martingale:", resultado_com_martingale)

    # Determinando a mais eficiente
    if resultado_sem_martingale > resultado_com_martingale:
        return "Sem martingale é a mais eficiente"
    elif resultado_sem_martingale < resultado_com_martingale:
        return "Com martingale é a mais eficiente"
    else:
        return "Ambas as opções são equivalentes"

# Chamando a função para comparar as possibilidades
melhor_situacao = comparar_possibilidades()

# Exibindo o resultado da comparação
print("Resultado:", melhor_situacao)
