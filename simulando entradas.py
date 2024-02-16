from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

erros_anterior = 0


def verificar_stop():
    stop_path = os.path.join(os.path.expanduser("~"), "Desktop", "stop.txt")
    return os.path.exists(stop_path)


def somar_resultados(acertos, erros, sequencia):
    global erros_anterior

    cores_anteriores = sequencia[1:4]
    cor_atual = sequencia[0]

    if all(cor == cores_anteriores[0] for cor in cores_anteriores) and cor_atual != cores_anteriores[0]:
        acertos += 1
        if erros_anterior == 1:  
            print(f"Acerto no Martingale !! Cor atual: {cor_atual}")
            erros_anterior = 0  
        else:
            print(f"Acerto !! Cor atual: {cor_atual}")
        return acertos, erros, 60  

    elif all(cor == cores_anteriores[0] for cor in cores_anteriores) and cor_atual == cores_anteriores[0]:
        erros_anterior += 1
        if erros_anterior == 1: 
            print(f"Erro !! Cor atual: {cor_atual}")
            return acertos, erros, 25  

        elif erros_anterior == 2:  
            print(f"Erro no Martingale !! Cor atual: {cor_atual}")
            erros_anterior = 0
            erros += 3
            return acertos, erros, 60  
        
        return acertos, erros, 25


    elif all(cor == cores_anteriores[0] for cor in cores_anteriores) and cor_atual == cores_anteriores[0]:
        erros_anterior += 1
        if erros_anterior == 1: 
            print("Erro !!")
            return acertos, erros, 25  

        elif erros_anterior == 2:  
            print("Erro no Martingale !!")
            erros_anterior = 0
            erros +=3
            return acertos, erros, 60  
        
    return acertos, erros, 25


def main():
    global erros_anterior

    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    resultados_path = os.path.join(desktop_path, "acertos_erros.txt")

    acertos, erros = 0, 0
    intervalo_contagem = 60  # Começa com 60 segundos

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
                "class").split()[-1] for box_element in box_elements[:5]]

            acertos, erros, intervalo_contagem = somar_resultados(
                acertos, erros, sequencia)

            with open(resultados_path, "w") as file:
                file.write(f"Acertos: {acertos}\nErros: {erros}\n")
                file.write(f"Segundos do loop atual: {intervalo_contagem}\n")
                file.write("Últimas 5 linhas:\n")
                file.write("\n".join(sequencia) + "\n")

            print(f"Segundos do loop atual: {intervalo_contagem}")

            time.sleep(intervalo_contagem)

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
