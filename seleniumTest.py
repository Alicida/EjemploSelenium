from selenium import webdriver
from pprint import pprint
import xlsxwriter
import time
driver = webdriver.Chrome(executable_path=r'../chromedriver.exe')
driver.get("https://www.tienda.movistar.com.mx/telefonos.html")
totalTelefonos = int(driver.find_element_by_xpath('//*[@id="toolbar-amount"]/span[3]').text)
telefonos = 0
arrayPhones = []
while telefonos != totalTelefonos:
    phones = driver.find_elements_by_class_name("grid__slot2")
    for phone in phones:
        array = {}
        array['nombre'] = phone.find_element_by_class_name("grid__title").text
        array['sku'] = phone.find_element_by_class_name("grid__ref").text
        gridvalueprice = phone.find_element_by_class_name("grid__value-price")
        children = gridvalueprice.find_element_by_xpath(".//*").text
        precioPospago = children
        array['precioPospago'] = round(float(precioPospago.replace("$", "")),2)*2*24
        array['precioPrepago'] = phone.find_element_by_class_name("price-wrapper").text;
        array['imagen'] = phone.find_element_by_class_name("grid__img").get_attribute('src')
        array['url'] = phone.find_element_by_class_name("grid__action").get_attribute('href')
        arrayPhones.append(array)
    telefonos += len(phones)
    paginador = driver.find_element_by_class_name('vass-page-numbers')
    paginas = paginador.find_elements_by_tag_name("li")
    bandera = 0
    for pagina in paginas:
        if bandera == 0:
            paginaclassname = pagina.get_attribute("class")
            if paginaclassname == 'item current':
                bandera = 1
        else:
            link = pagina.find_element_by_xpath(".//*")
            link.get_attribute('href')
            driver.get(link.get_attribute('href'))
            print('ya le dio clic')
            time.sleep(10)
            break
    print(telefonos)
    print(totalTelefonos)

workbook = xlsxwriter.Workbook('reporteTienda.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Nombre')
worksheet.write('B1', 'SKU')
worksheet.write('C1', 'Precio Pospago')
worksheet.write('D1', 'Precio Prepago')
worksheet.write('E1', 'Imagen')
worksheet.write('F1', 'Url')
col = 0
row = 1
for x in arrayPhones:
    worksheet.write(row, col, x['nombre'])
    worksheet.write(row, col + 1, x['sku'])
    worksheet.write(row, col + 2, x['precioPospago'])
    worksheet.write(row, col + 3, x['precioPrepago'])
    worksheet.write(row, col + 4, x['imagen'])
    worksheet.write(row, col + 5, x['url'])
    row += 1
    print ('Nombre: '+x['nombre']+', SKU: '+x['sku']+', Pospago: $'+str(x['precioPospago'])+', Prepago: '+x['precioPrepago'])
workbook.close()

driver.quit()
