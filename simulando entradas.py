from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time


def verificar_stop():
    stop_path = os.path.join(os.path.expanduser("~"), "Desktop", "stop.txt")
    return os.path.exists(stop_path)


def somar_resultados(acertos, erros, sequencia):
    cores_anteriores = sequencia[1:4]
    cor_atual = sequencia[0]

    if all(cor == cores_anteriores[0] for cor in cores_anteriores) and cor_atual != cores_anteriores[0]:
        acertos += 1
        print("Acerto!")
    elif all(cor == cores_anteriores[0] for cor in cores_anteriores) and cor_atual == cores_anteriores[0]:
        erros += 1
        print("Erro!")

    return acertos, erros


def main():
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    resultados_path = os.path.join(desktop_path, "acertos_erros.txt")

    acertos, erros = 0, 0
    acertos_anterior, erros_anterior = 0, 0
    intervalo_contagem = 15

    try:
        driver = webdriver.Chrome(service=service, options=options)
        url = 'https://blaze-7.com/pt/games/double'
        driver.get(url)

        while not verificar_stop():
            recent_results_element = driver.find_element(
                By.ID, "roulette-recent")
            box_elements = recent_results_element.find_elements(
                By.CLASS_NAME, "sm-box")

            sequencia = [box_element.get_attribute(
                "class").split()[-1] for box_element in box_elements[:4]]

            acertos, erros = somar_resultados(acertos, erros, sequencia)

            # Escrever resultados no arquivo a cada 60 segundos ou 15 segundos
            if acertos + erros > acertos_anterior + erros_anterior:
                with open(resultados_path, "w") as file:
                    file.write(f"Acertos: {acertos}\nErros: {erros}\n")
                    file.write("Últimas 4 linhas:\n")
                    file.write("\n".join(sequencia) + "\n")

                # Atualiza o número de acertos e erros do loop anterior
                acertos_anterior, erros_anterior = acertos, erros

                # Reinicia o contador de contagem para o próximo intervalo
                intervalo_contagem = 60
            else:
                # Decrementa o contador de contagem para o próximo loop
                intervalo_contagem = max(15, intervalo_contagem - 15)

            time.sleep(intervalo_contagem)

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
