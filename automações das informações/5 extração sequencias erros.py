import os

def extrair_texto(arquivo_entrada, arquivo_saida):
    try:
        # Caminho completo para o arquivo de entrada e saída
        caminho_entrada = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS", arquivo_entrada)
        caminho_saida = os.path.join(os.path.expanduser("~"), "Desktop", "LOGS", "jogadas.txt")
        
        with open(caminho_entrada, 'r') as entrada:
            linhas = entrada.readlines()
            
            # Encontrar a linha que contém "Possibilidades:"
            index_inicio = None
            for i, linha in enumerate(linhas):
                if "Possibilidades:" in linha:
                    index_inicio = i
                    break
            
            # Se não encontrar a palavra-chave, sai da função
            if index_inicio is None:
                print("Palavra-chave 'Possibilidades:' não encontrada no arquivo.")
                return
            
            # Extrair o texto a partir da linha encontrada
            texto = ''.join(linhas[index_inicio:])
            
            # Escrever o texto extraído no arquivo de saída
            with open(caminho_saida, 'w') as saida:
                saida.write(texto)
            
            print("Texto extraído com sucesso!")
    
    except FileNotFoundError:
        print("Arquivo de entrada não encontrado.")

# Nome do arquivo de entrada
arquivo_entrada = "resultados_erros_log_48.txt"

# Chamar a função para extrair o texto
extrair_texto(arquivo_entrada, "erros.txt")
