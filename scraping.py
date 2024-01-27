import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service()

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

url = 'https://blaze-7.com/pt/games/double?modal=double_history_index'
driver.get(url)

# Aguarda até que a classe history__double seja carregada
driver.implicitly_wait(10)

# Extrai informações da classe history__double
history_double_element = driver.find_element(By.CLASS_NAME, "history__double")
history_text = history_double_element.text

# Imprime as informações
print(history_text)

# Salva as informações em um arquivo de texto
with open("history_output.txt", "w", encoding="utf-8") as file:
    file.write(history_text)
