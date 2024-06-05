from collections import defaultdict
import os

def ler_dados(arquivo):
    with open(arquivo, 'r') as file:
        lines = file.readlines()
    return lines

def calcular_porcentagem_acerto(jogadas, acertos):
    porcentagens_acerto = defaultdict(dict)

    for jogada, acerto in zip(jogadas, acertos):
        jogada_sequencia, jogada_percentual = jogada.split(' - percentual (')
        jogada_sequencia = jogada_sequencia.strip().split(': ')[1]
        jogada_percentual = jogada_percentual.strip().split('): ')[0]
        jogada_quantidade = int(jogada.split('Quantidade: ')[1])

        acerto_sequencia, acerto_percentual = acerto.split(' - Quantidade: ')
        acerto_percentual = float(acerto_percentual.split(' - Quantidade: ')[0])
        acerto_quantidade = int(acerto.split('Quantidade: ')[1])

        if jogada_sequencia not in porcentagens_acerto:
            porcentagens_acerto[jogada_sequencia][jogada_percentual] = [0, 0]
        
        porcentagens_acerto[jogada_sequencia][jogada_percentual][0] += acerto_quantidade
        porcentagens_acerto[jogada_sequencia][jogada_percentual][1] += jogada_quantidade

    return porcentagens_acerto

def calcular_porcentagem(porcentagens_acerto):
    for sequencia, percentuais in porcentagens_acerto.items():
        print(f"\nSequencia: {sequencia}:")
        for percentual, quantidade in percentuais.items():
            porcentagem_acerto = quantidade[0] / quantidade[1] * 100 if quantidade[1] > 0 else 0
            print(f"  Percentual: {percentual} - Porcentagem de Acerto: {porcentagem_acerto:.2f}%")

def main():
    arquivo_jogadas = "confluencia_jogadas_100_direto_mod.txt"
    arquivo_acertos = "confluencia_acertos_100_direto_mod.txt"

    jogadas = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS","confluencias", "confluencia_jogadas_100_direto_mod.txt")
    acertos = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS", "confluencias", "confluencia_acertos_100_direto_mod.txt")

    porcentagens_acerto = calcular_porcentagem_acerto(jogadas, acertos)
    calcular_porcentagem(porcentagens_acerto)

if __name__ == "__main__":
    main()
