from selenium import webdriver
from bs4 import BeautifulSoup
from dados.config import settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import os

# Colocar isso em uma classe SuporteAutomato
driverlocation = r"chromedriver"
os.environ["webdriver.chrome.driver"]=driverlocation
driver = webdriver.Chrome()

# Colocar isso em uma classe PageObject ou algo do tipo
coluna_1=[]
coluna_2=[]
coluna_3=[]
coluna_4=[]
coluna_5=[]
coluna_6=[]
coluna_7=[]

driver.get(settings['url'])

driver.maximize_window()

txt_usuario = driver.find_element(By.ID, settings['elemento-usuario-id'])
txt_senha = driver.find_element(By.ID, settings['elemento-senha-id'])
btn_button = driver.find_element(By.ID, settings['elemento-botao-id'])

txt_usuario.send_keys(settings['usuario'])
txt_senha.send_keys(settings['senha'])
btn_button.click()

delay = 25 # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, settings['elemento-ancora'])))
    print("Página está pronta!!! :)")
except TimeoutException:
    print("Esperei demais :(")

content = driver.page_source
soup = BeautifulSoup(content, "lxml")

tables = soup.find("table", {"class": settings['classe-tabela']}).find("tbody")

for tr in tables.findAll("tr"):
    td = tr.findAll("td")
    if len(td) == 7:
        coluna_1.append(td[0].text.replace(',', ' '))
        coluna_2.append(td[1].text)
        coluna_3.append(td[2].text)
        coluna_4.append(td[3].text)
        coluna_5.append(td[4].text)
        coluna_6.append(td[5].text)
        coluna_7.append(td[6].text)

    print("Capturando dados da página...")
    
print("Copiando dados para o Excel...")
df = pd.DataFrame({settings['cabecalho-1']:coluna_1
                    ,settings['cabecalho-2']:coluna_2
                    ,settings['cabecalho-3']:coluna_3
                    ,settings['cabecalho-4']:coluna_4
                    ,settings['cabecalho-5']:coluna_5
                    ,settings['cabecalho-6']:coluna_6
                    ,settings['cabecalho-7']:coluna_7}) 
df.to_csv(settings['titulo-arquivo-gerado'], index=False, encoding=settings['encoding'])
print("Excel gerado com sucesso!!!")

driver.delete_all_cookies()
driver.quit()