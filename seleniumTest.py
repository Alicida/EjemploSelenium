from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import xlsxwriter
import time

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
# driver iniciará un navegador y abriá la url raíz.
driver.get("https://alicidafreak.blogspot.com/")

entradas = []
paginadorExiste = True

while paginadorExiste:

    # La variable de paso ents pretende ser una abreviación de entradas.
    ents = driver.find_elements(By.TAG_NAME, 'article')

    for ent in ents:
        entrada = {}
        entrada['fecha'] = ent.find_element(By.CLASS_NAME, 'published').text
        entrada['comentarios'] = ent.find_element(By.CLASS_NAME, 'num_comments').text
        contenedor = ent.find_element(By.CLASS_NAME, 'entry-title')
        entrada['titulo'] = contenedor.find_element(By.CLASS_NAME, 'r-snippetized').text        
        entrada['url'] = contenedor.find_element(By.TAG_NAME, 'a').get_attribute('href')
        entradas.append(entrada)
    
    if len(driver.find_elements(By.CLASS_NAME, 'blog-pager-older-link')) > 0:
        paginador=driver.find_element(By.CLASS_NAME, 'blog-pager-older-link')
        paginador.get_attribute('href')
        driver.get(paginador.get_attribute('href'))
        time.sleep(5)
    else:
        paginadorExiste = False

workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Título')
worksheet.write('B1', 'No. Comentarios')
worksheet.write('C1', 'Fecha Publicación')
worksheet.write('D1', 'URL Directa')
col = 0
row = 1

for e in entradas:
    worksheet.write(row, col, e['titulo'])
    worksheet.write(row, col + 1, e['comentarios'])
    worksheet.write(row, col + 2, e['fecha'])
    worksheet.write(row, col + 3, e['url'])
    row += 1

workbook.close()

driver.quit()
