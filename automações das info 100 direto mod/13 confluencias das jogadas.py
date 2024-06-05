import os

def extrair_dados(arquivo_entrada, arquivo_saida):
    with open(arquivo_entrada, 'r') as f:
        linhas = f.readlines()
        
        sequencias = []
        percentuais = {}
        
        i = 0
        while i < len(linhas):
            if "Ultimos 3 resultados:" in linhas[i]:
                try:
                    cor_atual = linhas[i].split(":")[1].strip().split(",")[0].strip()
                    cor_percentuais = linhas[i+1].split(":")[1].strip().split(", ")
                    percentual_cor_atual = float(cor_percentuais[["white", "black", "red"].index(cor_atual)])
                    sequencia = [
                        linhas[i + 5].split(":")[1].strip(),
                        linhas[i + 6].split(":")[1].strip(),
                        linhas[i + 7].split(":")[1].strip(),
                        linhas[i + 8].split(":")[1].strip()
                    ]
                    sequencia_str = ', '.join(sequencia)
                    percentual_cor_atual_str = str(percentual_cor_atual)

                    sequencias.append((sequencia_str, cor_atual, percentual_cor_atual_str))
                    
                    # Contagem de ocorrências de cada percentual
                    percentuais[percentual_cor_atual_str] = percentuais.get(percentual_cor_atual_str, 0) + 1
                    
                except (IndexError, ValueError):
                    pass
            i += 1

    # Escrever os dados extraídos no arquivo de saída
    with open(arquivo_saida, 'w') as out_file:
        for sequencia, cor_atual, percentual in sequencias:
            out_file.write(f"sequencia ({sequencia}) - percentual ({cor_atual}): {percentual}\n")
        
        # Escrever a contagem de sequências para cada percentual
        out_file.write("\nContagem de Sequências por Percentual:\n")
        for percentual, quantidade in percentuais.items():
            out_file.write(f"Percentual ({percentual}): {quantidade}\n")

# Caminhos dos arquivos de entrada e saída
arquivo_entrada = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS", "resultados", "resultados_100 direto mod.txt")
arquivo_saida = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS", "confluencia_jogadas_100_direto_mod.txt")

# Remova o arquivo de saída se já existir
if os.path.exists(arquivo_saida):
    os.remove(arquivo_saida)

# Chamar a função para extrair dados
extrair_dados(arquivo_entrada, arquivo_saida)

print("Informações confluentes salvas em 'confluencia_jogadas_100_direto_mod.txt'.")
