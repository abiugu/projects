import pygame
import time
import os


def pre_entrada():
    # Inicializa o pygame
    pygame.init()

    # Caminho para o arquivo de som
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    som_path = os.path.join(desktop_path, "MONEY ALARM.mp3")

    # Carrega o som de alerta
    pygame.mixer.music.load(som_path)

    # Define o volume do som
    pygame.mixer.music.set_volume(1.0)

    # Reproduz o som de alerta
    pygame.mixer.music.play()

    # Aguarda 10 segundos
    time.sleep(10)

    # Para a reprodução do som
    pygame.mixer.music.stop()

    # Encerra o pygame
    pygame.quit()


# Chama a função pre_entrada para sinalizar a pré-entrada
pre_entrada()
