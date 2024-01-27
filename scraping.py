import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = service()

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)
