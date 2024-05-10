import os

# Define o caminho para o arquivo de log
caminho_arquivo = os.path.join(os.path.expanduser('~'), 'Desktop', 'LOGS', 'log 48.txt')

# Função para extrair os maiores valores de acertos diretos e acertos de gale de cada sequência de buscas
# e contar quantas vezes o "white" foi visto após um alarme
def extrair_maiores_acertos_e_contar_white(arquivo_log):
    maiores_acertos_diretos = []
    maiores_acertos_gale = []
    white_visto_apos_alarme = False
    contador_white_apos_alarme = 0
    maior_acerto_direto_atual = 0
    maior_acerto_gale_atual = 0
    with open(arquivo_log, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            if 'Acertos direto:' in linha:
                acertos_diretos = int(linha.split('Acertos direto: ')[1].split(',')[0])
                if acertos_diretos > maior_acerto_direto_atual:
                    maior_acerto_direto_atual = acertos_diretos
            elif 'Acertos gale:' in linha:
                acertos_gale = int(linha.split('Acertos gale: ')[1].split(',')[0])
                if acertos_gale > maior_acerto_gale_atual:
                    maior_acerto_gale_atual = acertos_gale
            elif 'Alarme acionado' in linha:
                if white_visto_apos_alarme:
                    contador_white_apos_alarme += 1
                    white_visto_apos_alarme = False
            elif 'white' in linha:
                if not white_visto_apos_alarme:
                    white_visto_apos_alarme = True
    # Se houver um maior_acerto_atual pendente no final do arquivo, adiciona à lista
    if maior_acerto_direto_atual > 0:
        maiores_acertos_diretos.append(maior_acerto_direto_atual)
    if maior_acerto_gale_atual > 0:
        maiores_acertos_gale.append(maior_acerto_gale_atual)
    return maiores_acertos_diretos, maiores_acertos_gale, contador_white_apos_alarme

# Extrai os maiores valores de acertos diretos e acertos de gale de cada sequência de buscas
# e conta quantas vezes o "white" foi visto após um alarme
maiores_acertos_diretos, maiores_acertos_gale, contador_white_apos_alarme = extrair_maiores_acertos_e_contar_white(caminho_arquivo)

# Soma os maiores valores de acertos diretos e acertos de gale
total_maiores_acertos_diretos = sum(maiores_acertos_diretos)
total_maiores_acertos_gale = sum(maiores_acertos_gale)

# Imprime o total dos maiores valores de acertos diretos e acertos de gale
print("Total dos maiores valores de acertos diretos:", total_maiores_acertos_diretos)
print("Total dos maiores valores de acertos de gale:", total_maiores_acertos_gale)
print("Número de vezes que 'white' foi visto após um alarme:", contador_white_apos_alarme)
