import os
import re
from openpyxl import Workbook

def ler_e_analisar_log(caminho_arquivo_log):
    with open(caminho_arquivo_log, 'r') as f:
        log_data = f.read()

    resultados_re = re.compile(r'Ultimos 3 resultados: (\w+), (\w+), (\w+)')
    percentuais_re = re.compile(r'percentual cor atual: ([\d.]+)%')
    porcentagens_25_re = re.compile(r'Ultimas 25 porcentagens: ([<>=])')
    porcentagens_50_re = re.compile(r'Ultimas 50 porcentagens: ([<>=])')
    porcentagens_100_re = re.compile(r'Ultimas 100 porcentagens: ([<>=])')
    porcentagens_500_re = re.compile(r'Ultimas 500 porcentagens: ([<>=])')
    acertos_re = re.compile(r'acertos: (\d+)')
    total_re = re.compile(r'total: (\d+)')
    assertividade_re = re.compile(r'assertividade: ([\d.]+)%')

    resultados = resultados_re.findall(log_data)
    percentuais = percentuais_re.findall(log_data)
    porcentagens_25 = porcentagens_25_re.findall(log_data)
    porcentagens_50 = porcentagens_50_re.findall(log_data)
    porcentagens_100 = porcentagens_100_re.findall(log_data)
    porcentagens_500 = porcentagens_500_re.findall(log_data)
    acertos = acertos_re.findall(log_data)
    total = total_re.findall(log_data)
    assertividade = assertividade_re.findall(log_data)

    return resultados, percentuais, porcentagens_25, porcentagens_50, porcentagens_100, porcentagens_500, acertos, total, assertividade

def processar_dados(resultados, percentuais, porcentagens_25, porcentagens_50, porcentagens_100, porcentagens_500, acertos, total, assertividade):
    dados_agrupados = {}

    min_length = min(len(resultados), len(percentuais), len(porcentagens_25), len(porcentagens_50), len(porcentagens_100), len(porcentagens_500), len(acertos), len(total), len(assertividade))

    for i in range(min_length):
        percentual = float(percentuais[i])
        sinal_25 = porcentagens_25[i] if i < len(porcentagens_25) else ''
        sinal_50 = porcentagens_50[i] if i < len(porcentagens_50) else ''
        sinal_100 = porcentagens_100[i] if i < len(porcentagens_100) else ''
        sinal_500 = porcentagens_500[i] if i < len(porcentagens_500) else ''
        total_acertos = int(acertos[i])
        total_jogadas = int(total[i])

        chave = (percentual, sinal_25, sinal_50, sinal_100, sinal_500)

        if chave not in dados_agrupados:
            dados_agrupados[chave] = {
                'total_acertos': 0,
                'total_jogadas': 0
            }

        dados_agrupados[chave]['total_acertos'] += total_acertos
        dados_agrupados[chave]['total_jogadas'] += total_jogadas

    for chave, dados in dados_agrupados.items():
        percentual, sinal_25, sinal_50, sinal_100, sinal_500 = chave
        total_acertos = dados['total_acertos']
        total_jogadas = dados['total_jogadas']
        assertividade = (total_acertos / total_jogadas) * 100 if total_jogadas > 0 else 0.0
        dados_agrupados[chave]['assertividade'] = assertividade

    return dados_agrupados

def criar_planilha(dados_agrupados, caminho_arquivo_excel):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Análise de Dados'

    header = ["Percentual", "Comparação 25", "Comparação 50", "Comparação 100", "Comparação 500", "Acertos", "Total", "Assertividade (%)"]
    sheet.append(header)

    for (percentual, sinal_25, sinal_50, sinal_100, sinal_500), dados in dados_agrupados.items():
        total_acertos = dados['total_acertos']
        total_jogadas = dados['total_jogadas']
        assertividade = dados['assertividade']
        row = [percentual, sinal_25, sinal_50, sinal_100, sinal_500, total_acertos, total_jogadas, f"{assertividade:.2f}"]
        sheet.append(row)

    workbook.save(caminho_arquivo_excel)
    print(f"Planilha Excel gerada com sucesso em: {caminho_arquivo_excel}")

def main():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    caminho_arquivo_log = os.path.join(desktop_path, 'previsoes_quebras_padrao.txt')
    caminho_arquivo_excel = os.path.join(desktop_path, 'LOGS', 'Dados log global.xlsx')

    resultados, percentuais, porcentagens_25, porcentagens_50, porcentagens_100, porcentagens_500, acertos, total, assertividade = ler_e_analisar_log(caminho_arquivo_log)
    dados_agrupados = processar_dados(resultados, percentuais, porcentagens_25, porcentagens_50, porcentagens_100, porcentagens_500, acertos, total, assertividade)
    criar_planilha(dados_agrupados, caminho_arquivo_excel)

if __name__ == "__main__":
    main()
