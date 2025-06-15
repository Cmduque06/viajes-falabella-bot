# BOT para automatizar la búsqueda de paquetes en Viajes Falabella

import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Configuración de opciones de Chrome en incógnito
chrome_options = Options()
chrome_options.add_argument("--incognito")

# Inicializa el navegador Chrome en modo incógnito
driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. Ingresa al sitio web de Viajes Falabella
    driver.get("https://www.viajesfalabella.com.co/")
    time.sleep(3)

    # 2. Selecciona la opción de Paquetes
    paquetes_btn = driver.find_element(By.XPATH, "/html/body/div[2]/nav/div[2]/div/div[3]/ul/li[3]/a")
    paquetes_btn.click()
    time.sleep(3)

    # 3. Ingresa aeropuerto de origen
    origen_input = driver.find_element(By.XPATH, "/html/body/app-root/div/header-wrapper/header-view-1/div/div/sbox/div/div/searchbox-v2/div/div/div/div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/div/div/input")
    origen_input.clear()
    origen_input.send_keys("Jose Maria Cordova")
    time.sleep(3)
    origen_input.send_keys(Keys.ENTER)
    
    

    # 4. Ingresa aeropuerto de destino
    destino_input = driver.find_element(By.XPATH, "/html/body/app-root/div/header-wrapper/header-view-1/div/div/sbox/div/div/searchbox-v2/div/div/div/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/div/input")
    destino_input.clear()
    destino_input.send_keys("Aruba")
    time.sleep(5)
    destino_input.send_keys(Keys.ENTER)

    # 5. Selecciona fechas
    # a. Haz clic en el campo de fechas
    driver.find_element(By.XPATH, "/html/body/app-root/div/header-wrapper/header-view-1/div/div/sbox/div/div/searchbox-v2/div/div/div/div/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div/div").click()
    time.sleep(3)

    
    driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/a[2]").click()
    time.sleep(3)
    # b. Selecciona fecha de salida: 29 de julio
    fecha_salida = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[2]/div/div[2]/div[3]/div[29]')
    fecha_salida.click()
    time.sleep(3)

    # c. Selecciona fecha de regreso: 21 de agosto
    fecha_regreso = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div[2]/div/div[2]/div[3]/div[21]')
    fecha_regreso.click()
    time.sleep(3)

    # d. Haz click en "Aplicar" para las fechas
    driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[3]/div[1]/button[2]").click()
    time.sleep(3)

    # 6. Configura habitaciones y pasajeros
    # a. Haz click en el campo de habitaciones y personas
    driver.find_element(By.XPATH, "/html/body/app-root/div/header-wrapper/header-view-1/div/div/sbox/div/div/searchbox-v2/div/div/div/div/div/div/div/div[2]/div[1]/div[3]/div/div").click()
    time.sleep(3)

    # b. Añadir una habitación extra
    #driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[2]/div/div[2]/div[3]/div[21]").click()
    #time.sleep(3)

    # c. Añadir 2 personas a la habitación 1 (debe quedar en 4 adultos)
    for _ in range(2):
        driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/button[2]").click()
        time.sleep(2)

    # d. Haz clic en "Aplicar" para habitaciones
    driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div/div[2]/button[2]").click()
    time.sleep(3)

    # 7. Realizar la búsqueda
    driver.find_element(By.XPATH, "/html/body/app-root/div/header-wrapper/header-view-1/div/div/sbox/div/div/searchbox-v2/div/div/div/div/div/div/div/div[2]/div[1]/div[4]/button").click()
    time.sleep(20)

    # 8. Extraer los resultados de la primera búsqueda
    resultados = driver.find_element(By.XPATH, "/html/body/aloha-app-root/aloha-results/div[2]/div/div/div/div[2]/div[2]/div/aloha-list-view-container")

    # 9. Aplicar el filtro "Desayuno incluido"
    driver.find_element(By.XPATH, "/html/body/aloha-app-root/aloha-results/div[2]/div/div/div/div[2]/div[1]/aloha-filter-list/div/ul/li[4]/aloha-filter/aloha-checkbox-filter/ul/li[1]/span").click()
    time.sleep(10)

    # Aplicar el filtro "4 estrellas"
    driver.find_element(By.XPATH, "/html/body/aloha-app-root/aloha-results/div[2]/div/div/div/div[2]/div[1]/aloha-filter-list/div/ul/li[4]/aloha-filter/aloha-checkbox-filter/ul/li[2]/span").click()
    time.sleep(10)

    # 10. Extrae los resultados después de aplicar el filtro
    resultados_filtrados = driver.find_element(By.XPATH, "/html/body/aloha-app-root/aloha-results/div[2]/div/div/div/div[2]/div[2]/div")

    # 11. Extrae precios de los paquetes en la primera página
    paquetes = driver.find_elements(By.XPATH, "//div[contains(@class, 'package-card')]")
    precios = []
    for paquete in paquetes:
        precio = paquete.find_element(By.XPATH, ".//span[contains(@class, 'main-value')]").text
        precios.append({"precio": precio})

    # 12. Guarda los precios en un archivo JSON
    with open("precios_paquetes.json", "w", encoding="utf-8") as f:
        json.dump(precios, f, ensure_ascii=False, indent=4)

    # 13. Ir al footer y hacer click en el WhatsApp
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    whatsapp_link = driver.find_element(By.XPATH, "//a[contains(@href, 'whatsapp')]")
    whatsapp_link.click()
    time.sleep(2)

    # 14. Tomar una screenshot
    driver.save_screenshot("whatsapp_contacto.png")

finally:
    # 15. Cerrar pantalla
    driver.quit()