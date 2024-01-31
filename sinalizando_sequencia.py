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
                mensagem_sequencia = f"{datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S')} - Sem sequências"
            else:
                current_line_color = lines[0].split(
                    ",")[1].split(":")[1].strip()

                i = 1
                while i < len(lines) and lines[i].split(",")[1].split(":")[1].strip() == current_line_color:
                    i += 1

                quantidade_sequencia = max(0, i - 1)
                mensagem_sequencia = (
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                    f"Sequência de {
                        quantidade_sequencia} cores iguais encontrada!"
                ) if quantidade_sequencia >= 3 else f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Sem sequências"

            # Ler a lista de mensagens registradas
            existing_content = sinal_file.readlines()

            # Verificar se a última mensagem é a mesma da mensagem atual
            last_sequence_message = existing_content[0].strip().split(" - ")[1]
            current_sequence_message = mensagem_sequencia.split(" - ")[1]

            if current_sequence_message != last_sequence_message:
                # Voltar para o início do arquivo antes de escrever
                sinal_file.seek(0)
                sinal_file.truncate()
                sinal_file.write(
                    "\n".join([mensagem_sequencia] + existing_content))

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
