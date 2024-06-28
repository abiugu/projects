import os
import re
from collections import defaultdict
from openpyxl import Workbook

def ler_e_analisar_log(caminho_arquivo_log):
    with open(caminho_arquivo_log, 'r') as f:
        log_data = f.read()
    
    resultados_re = re.compile(r'Ultimos 3 resultados: (\w+), (\w+), (\w+)')
    porcentagens_25_re = re.compile(r'Ultimas 25 porcentagens: ([\d.]+), ([\d.]+), ([\d.]+)')
    porcentagens_50_re = re.compile(r'Ultimas 50 porcentagens: ([\d.]+), ([\d.]+), ([\d.]+)')
    porcentagens_100_re = re.compile(r'Ultimas 100 porcentagens: ([\d.]+), ([\d.]+), ([\d.]+)')
    porcentagens_500_re = re.compile(r'Ultimas 500 porcentagens: ([\d.]+), ([\d.]+), ([\d.]+)')
    
    resultados = resultados_re.findall(log_data)
    porcentagens_25 = porcentagens_25_re.findall(log_data)
    porcentagens_50 = porcentagens_50_re.findall(log_data)
    porcentagens_100 = porcentagens_100_re.findall(log_data)
    porcentagens_500 = porcentagens_500_re.findall(log_data)
    
    return resultados, porcentagens_25, porcentagens_50, porcentagens_100, porcentagens_500

def comparar_percentuais(atual, oposta):
    if atual > oposta:
        return '>'
    elif atual < oposta:
        return '<'
    else:
        return '='

def calcular_assertividade(total_acertos, total):
    return round((total_acertos / total) * 100, 2) if total > 0 else 0.00

def analisar_padroes(resultados, porcentagens_25, porcentagens_50, porcentagens_100, porcentagens_500):
    padroes_agrupados = {}

    for i in range(len(resultados) - 1):
        cor_atual = resultados[i][0]
        if resultados[i][0] == resultados[i][1] == resultados[i][2]:
            try:
                porcentagem_atual_25 = float(porcentagens_25[i][2])
                porcentagem_oposta_25 = float(porcentagens_25[i][1])
                porcentagem_atual_50 = float(porcentagens_50[i][2])
                porcentagem_oposta_50 = float(porcentagens_50[i][1])
                porcentagem_atual_100 = float(porcentagens_100[i][2])
                porcentagem_oposta_100 = float(porcentagens_100[i][1])
                porcentagem_atual_500 = float(porcentagens_500[i][2])
                porcentagem_oposta_500 = float(porcentagens_500[i][1])
                
            except IndexError:
                continue

            comparacao_25 = comparar_percentuais(porcentagem_atual_25, porcentagem_oposta_25)
            comparacao_50 = comparar_percentuais(porcentagem_atual_50, porcentagem_oposta_50)
            comparacao_100 = comparar_percentuais(porcentagem_atual_100, porcentagem_oposta_100)
            comparacao_500 = comparar_percentuais(porcentagem_atual_500, porcentagem_oposta_500)

            chave_padrao = (porcentagem_atual_25, comparacao_25, comparacao_50, comparacao_100, comparacao_500)
            
            if chave_padrao not in padroes_agrupados:
                padroes_agrupados[chave_padrao] = {
                    'percentual': porcentagem_atual_25,
                    'comparacoes': (comparacao_25, comparacao_50, comparacao_100, comparacao_500),
                    'total_acertos': 0,
                    'total': 0
                }
            
            acerto = resultados[i + 1][0] != cor_atual
            padroes_agrupados[chave_padrao]['total'] += 1
            if acerto:
                padroes_agrupados[chave_padrao]['total_acertos'] += 1

    for dados in padroes_agrupados.values():
        dados['assertividade'] = calcular_assertividade(dados['total_acertos'], dados['total'])

    return padroes_agrupados

def main():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    arquivo_log = os.path.join(desktop_path, 'LOGS', 'log global.txt')
    
    resultados, porcentagens_25, porcentagens_50, porcentagens_100, porcentagens_500 = ler_e_analisar_log(arquivo_log)
    padroes_agrupados = analisar_padroes(resultados, porcentagens_25, porcentagens_50, porcentagens_100, porcentagens_500)
    
    arquivo_excel = os.path.join(desktop_path, 'dados log global.xlsx')
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Análise de Comparações'

    header = ["Percentual", "Comparação 25", "Comparação 50", "Comparação 100", "Comparação 500", "Acertos", "Total", "Assertividade (%)"]
    sheet.append(header)

    for dados in padroes_agrupados.values():
        percentual, comparacoes, total_acertos, total, assertividade = (
            dados['percentual'], 
            dados['comparacoes'], 
            dados['total_acertos'], 
            dados['total'],
            dados['assertividade']
        )
        assertividade_formatada = f"{assertividade:.2f}"  # Formata a assertividade com duas casas decimais
        
        # Filtro para incluir apenas linhas com assertividade maior que 50%
        if assertividade > 50:
            row = [percentual] + list(comparacoes) + [total_acertos, total, assertividade_formatada]
            sheet.append(row)

    workbook.save(arquivo_excel)
    print(f"Planilha Excel gerada com sucesso em: {arquivo_excel}")

if __name__ == "__main__":
    main()
