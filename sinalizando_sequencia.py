import os
import time
from datetime import datetime

# Caminho completo do arquivo .txt na área de trabalho
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
txt_file_path = os.path.join(desktop_path, "resultados_recentes.txt")
sinal_file_path = os.path.join(desktop_path, "sinal_sequencias.txt")
stop_file_path = os.path.join(desktop_path, "stop.txt")

# Função para verificar sequências e escrever em um arquivo


def verificar_sequencias():
    try:
        # Ler todas as linhas do arquivo
        with open(txt_file_path, "r") as txt_file, open(sinal_file_path, "r+") as sinal_file:
            lines = txt_file.readlines()

            if len(lines) < 1:
                return  # Não há sequência suficiente

            sequencia_cores = ["preto", "vermelho", "branco"]

            current_line_color = lines[0].split(",")[1].split(":")[1].strip()
            quantidade_sequencia = 1

            for i in range(1, len(lines)):  # Iterar desde a segunda linha
                next_line_color = lines[i].split(",")[1].split(":")[1].strip()

                if next_line_color == current_line_color:
                    quantidade_sequencia += 1
                else:
                    break  # Se a sequência for quebrada, parar

            # Atualizar a mensagem no arquivo de sinalizações
            with open(sinal_file_path, "r+") as sinal_file:
                existing_content = sinal_file.read()
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if quantidade_sequencia >= 3:
                    mensagem_sequencia = f"{
                        current_datetime} - Sequência de {quantidade_sequencia} cores iguais encontrada!\n"

                    if mensagem_sequencia not in existing_content:
                        sinal_file.seek(0)
                        sinal_file.write(mensagem_sequencia + existing_content)
                else:
                    mensagem_sem_sequencia = f"{
                        current_datetime} - Sem sequências\n"

                    if mensagem_sem_sequencia not in existing_content:
                        sinal_file.seek(0)
                        sinal_file.write(
                            mensagem_sem_sequencia + existing_content)

            # Verificar se o arquivo "stop.txt" existe
            if os.path.exists(stop_file_path):
                print("Parando o código.")
                exit()

    except Exception as e:
        print(f"Erro: {e}")


# Loop infinito para verificar sequências continuamente
while True:
    verificar_sequencias()
    time.sleep(5)  # Espera 5 segundos antes de verificar novamente
