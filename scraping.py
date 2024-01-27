import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service()

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)

url = 'https://blaze-7.com/pt/games/double?modal=double_history_index'
driver.get(url)

# Aguarda até que o elemento com o ID history__double seja carregado
driver.implicitly_wait(10)

# Extrai informações do elemento com o ID history__double
history_double_element = driver.find_element(By.ID, "history__double")
history_text = history_double_element.text

# Imprime as informações
print(history_text)

# Salva as informações em um arquivo de texto
with open("history_output.txt", "w", encoding="utf-8") as file:
    file.write(history_text)
