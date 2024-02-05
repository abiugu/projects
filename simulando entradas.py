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

    if len(sequencia) >= 4:
        if all(cor == cores_anteriores[0] for cor in cores_anteriores) and cor_atual == cores_anteriores[0]:
            erros += 1
            print("Erro!")
        elif all(cor == cores_anteriores[0] for cor in cores_anteriores) and cor_atual != cores_anteriores[0]:
            acertos += 1
            print("Acerto!")

    return acertos, erros


def main():
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    txt_file_path = os.path.join(desktop_path, "resultados_recentes.txt")
    resultados_path = os.path.join(desktop_path, "acertos_erros.txt")

    acertos, erros = 0, 0
    resultados_anteriores = {"acertos": 0,
                             "erros": 0, "ultimas_tres_linhas": []}

    try:
        driver = webdriver.Chrome(service=service, options=options)
        url = 'https://blaze-7.com/pt/games/double'
        driver.get(url)

        while not verificar_stop():
            recent_results_element = driver.find_element(
                By.ID, "roulette-recent")
            box_elements = recent_results_element.find_elements(
                By.CLASS_NAME, "sm-box")

            sequencia = []
            for i, box_element in enumerate(box_elements[:4]):
                color = box_element.get_attribute("class").split()[-1]
                sequencia.append(color)

            acertos, erros = somar_resultados(acertos, erros, sequencia)

            # Escrever resultados no arquivo
            with open(resultados_path, "w") as file:
                file.write(f"Acertos: {acertos}\nErros: {erros}\n")
                file.write("Últimas 4 linhas:\n")
                for linha in resultados_anteriores['ultimas_tres_linhas']:
                    file.write(f"{linha}\n")

            resultados_anteriores['acertos'] = acertos
            resultados_anteriores['erros'] = erros
            resultados_anteriores['ultimas_tres_linhas'] = sequencia

            # Definir o intervalo com base em acerto ou erro
            if acertos > resultados_anteriores['acertos'] or erros > resultados_anteriores['erros']:
                intervalo = 60  # Intervalo de 60 segundos em caso de acerto ou erro
            else:
                intervalo = 20  # Intervalo de 20 segundos em caso de nenhum acerto ou erro

            print(f"Aguardando {intervalo} segundos...")
            time.sleep(intervalo)

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
