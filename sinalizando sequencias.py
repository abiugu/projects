import os
import time

# Caminho completo do arquivo .txt na área de trabalho
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
txt_file_path = os.path.join(desktop_path, "resultados_recentes.txt")
sinal_file_path = os.path.join(desktop_path, "sinal_sequencias.txt")

# Função para verificar sequências e escrever em um arquivo


def verificar_sequencias():
    try:
        # Ler todas as linhas do arquivo
        with open(txt_file_path, "r") as txt_file, open(sinal_file_path, "r+") as sinal_file:
            lines = txt_file.readlines()

            sequencia_cores = ["preto", "vermelho"]
            quantidade_sequencia = 0
            sequencia_iniciada = False

            # Iterar do último para o primeiro elemento
            for i in range(len(lines)-2, -1, -1):
                current_line_color = lines[i].split(
                    ",")[1].split(":")[1].strip()

                # Iniciar a sequência se a cor não for branca
                if current_line_color != "branco" and not sequencia_iniciada:
                    sequencia_iniciada = True

                if sequencia_iniciada:
                    next_line_color = lines[i +
                                            1].split(",")[1].split(":")[1].strip()
                    next_next_line_color = lines[i +
                                                 2].split(",")[1].split(":")[1].strip()

                    # Verificar sequência apenas se a cor não for branca
                    if current_line_color != "branco" and next_line_color != "branco" and next_next_line_color != "branco":
                        if all(color in sequencia_cores for color in [current_line_color, next_line_color, next_next_line_color]):
                            quantidade_sequencia += 1

            # Ler a quantidade atual de sequências do arquivo
            sinal_file.seek(0)
            conteudo = sinal_file.read()
            sinal_file.seek(0)

            # Atualizar a mensagem no arquivo de sinalizações (apenas a primeira linha)
            sinal_file.write(
                f"Sequência de {quantidade_sequencia} cores iguais encontrada!\n")
            sinal_file.write(conteudo)

            # Truncar o arquivo após a primeira linha
            sinal_file.truncate()

    except Exception as e:
        print(f"Erro: {e}")


# Loop infinito para verificar sequências continuamente
while True:
    verificar_sequencias()
    time.sleep(5)  # Espera 5 segundos antes de verificar novamente
