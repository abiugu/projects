import os
import re
from collections import defaultdict

# Função para ler e analisar o log
def ler_e_analisar_log(caminho_arquivo_log):
    with open(caminho_arquivo_log, 'r') as f:
        log_data = f.read()
    
    # Expressões regulares para capturar os dados necessários
    ultimos_resultados_re = re.compile(r'Ultimos 3 resultados: (\w+), (\w+), (\w+)')
    porcentagens_re = re.compile(r'Ultimas (\d+) porcentagens: ([\d.]+), ([\d.]+), ([\d.]+)')
    
    resultados = ultimos_resultados_re.findall(log_data)
    porcentagens = porcentagens_re.findall(log_data)
    
    return resultados, porcentagens

# Função para analisar os padrões e calcular as probabilidades
def analisar_padroes(resultados, porcentagens):
    padroes = defaultdict(list)
    
    for i in range(len(resultados) - 1):
        padrao_atual = (resultados[i], tuple(porcentagens[i*4:(i*4)+4]))
        proximo_resultado = resultados[i + 1]
        
        padroes[padrao_atual].append(proximo_resultado)
    
    analise = {}
    for padrao, resultados_seguinte in padroes.items():
        total_ocorrencias = len(resultados_seguinte)
        contagem_resultados = defaultdict(int)
        
        for resultado in resultados_seguinte:
            contagem_resultados[resultado] += 1
        
        porcentagens_resultados = {res: (cont / total_ocorrencias) * 100 for res, cont in contagem_resultados.items()}
        analise[padrao] = porcentagens_resultados
    
    return analise

# Função para fazer predições com base na análise
def fazer_predicoes(analise, padrao_atual):
    if padrao_atual in analise:
        predicoes = analise[padrao_atual]
        predicoes_str = []
        for resultado, porcentagem in predicoes.items():
            predicoes_str.append(f"Com {porcentagem:.2f}% de chance, a próxima jogada será: {resultado}")
        return predicoes_str
    else:
        return ["Padrão atual não encontrado na análise de dados."]

# Função principal para executar a análise, predição e salvar em arquivo
def main():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    arquivo_log = os.path.join(desktop_path, 'LOGS', 'log 100 modded.txt')
    
    resultados, porcentagens = ler_e_analisar_log(arquivo_log)
    analise = analisar_padroes(resultados, porcentagens)
    
    # Exemplo de padrão atual (este seria dinâmico na prática)
    padrao_atual = (('red', 'red', 'red'), (('25', '12.0', '40.0', '44.0'), ('50', '10.0', '44.0', '44.0'), ('100', '8.0', '44.0', '48.0'), ('500', '7.6', '46.6', '45.6')))
    
    predicoes = fazer_predicoes(analise, padrao_atual)
    
    arquivo_previsoes = os.path.join(desktop_path, 'previsoes.txt')
    
    # Salvar previsões em arquivo
    with open(arquivo_previsoes, 'w') as f:
        for predicao in predicoes:
            f.write(predicao + '\n')
    
    # Calcular e salvar as porcentagens de assertividade
    total_padroes = len(analise)
    assertividade = {}
    
    for padrao, predicoes in analise.items():
        for resultado, porcentagem in predicoes.items():
            if resultado not in assertividade:
                assertividade[resultado] = []
            assertividade[resultado].append(porcentagem)
    
    with open(arquivo_previsoes, 'a') as f:
        f.write('\nPorcentagens de assertividade:\n')
        for resultado, porcentagens in assertividade.items():
            media_porcentagem = sum(porcentagens) / len(porcentagens)
            f.write(f"{resultado}: {media_porcentagem:.2f}%\n")

if __name__ == "__main__":
    main()
