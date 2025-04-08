import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Crear carpeta de capturas si no existe
if not os.path.exists("capturas"):
    os.makedirs("capturas")

inicio_total = time.time()
fecha_generacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Crear reporte HTML
reporte = open("reporte.html", "w", encoding="utf-8")
reporte.write(f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Pruebas</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
            color: #333;
        }}
        h1 {{
            color: #005588;
            text-align: center;
        }}
        .escenario {{
            background-color: #fff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .success {{
            color: green;
            font-weight: bold;
        }}
        .error {{
            color: red;
            font-weight: bold;
        }}
        img {{
            margin-top: 10px;
            border: 1px solid #ccc;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <h1>Reporte de Pruebas Automatizadas</h1>
    <p><strong>Fecha de generación:</strong> {fecha_generacion}</p>
""")

# Iniciar navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("http://127.0.0.1:5500/")
time.sleep(2)

# Funciones para cada escenario
def agregar_vehiculo(driver):
    driver.find_element(By.ID, "brand").send_keys("Acura")
    driver.find_element(By.ID, "model").send_keys("RSX")
    driver.find_element(By.ID, "year").send_keys("2003")
    driver.find_element(By.ID, "price").send_keys("6000")
    driver.find_element(By.ID, "color").send_keys("Blanco")
    driver.find_element(By.ID, "save-btn").click()
    time.sleep(2)

def editar_vehiculo(driver):
    time.sleep(1)
    editar_btns = driver.find_elements(By.XPATH, "//button[contains(text(),'Editar')]")
    editar_btns[-1].click()
    time.sleep(1)
    campo_modelo = driver.find_element(By.ID, "model")
    campo_modelo.clear()
    campo_modelo.send_keys("RSX Type S")
    driver.find_element(By.ID, "save-btn").click()
    time.sleep(2)

def eliminar_vehiculo(driver):
    eliminar_btn = driver.find_elements(By.XPATH, "//button[contains(text(),'Eliminar')]")[0]
    eliminar_btn.click()
    time.sleep(1)

def limpiar_formulario(driver):
    driver.find_element(By.ID, "brand").send_keys("Toyota")
    driver.find_element(By.ID, "model").send_keys("Vitz GR")
    driver.find_element(By.ID, "year").send_keys("2017")
    driver.find_element(By.ID, "price").send_keys("8000")
    driver.find_element(By.ID, "color").send_keys("Negro")
    driver.find_element(By.ID, "clear-btn").click()
    time.sleep(1)
    assert driver.find_element(By.ID, "brand").get_attribute("value") == ""
    assert driver.find_element(By.ID, "model").get_attribute("value") == ""
    assert driver.find_element(By.ID, "year").get_attribute("value") == ""
    assert driver.find_element(By.ID, "price").get_attribute("value") == ""
    assert driver.find_element(By.ID, "color").get_attribute("value") == ""

# Lista de escenarios
escenarios = [
    {
        "titulo": "1. Agregar Vehículo",
        "archivo": "agregar.png",
        "accion": lambda: agregar_vehiculo(driver)
    },
    {
        "titulo": "2. Editar Vehículo",
        "archivo": "editar.png",
        "accion": lambda: editar_vehiculo(driver)
    },
    {
        "titulo": "3. Eliminar Vehículo",
        "archivo": "eliminar.png",
        "accion": lambda: eliminar_vehiculo(driver)
    },
    {
        "titulo": "4. Limpiar Formulario",
        "archivo": "limpiar.png",
        "accion": lambda: limpiar_formulario(driver)
    },
]

# Ejecutar escenarios
for escenario in escenarios:
    reporte.write(f"<div class='escenario'><h2>{escenario['titulo']}</h2>")
    inicio = time.time()
    try:
        escenario["accion"]()
        duracion = time.time() - inicio
        captura = f"capturas/{escenario['archivo']}"
        driver.save_screenshot(captura)
        reporte.write(f"<p class='success'>✅ Escenario Completado con Éxito</p>")
        reporte.write(f"<p>⏱️ Duración: {duracion:.2f} segundos</p>")
        reporte.write(f"<img src='{captura}' width='500'><br>")
    except Exception as e:
        duracion = time.time() - inicio
        captura = f"capturas/error_{escenario['archivo']}"
        driver.save_screenshot(captura)
        reporte.write(f"<p class='error'>❌ Error: {e}</p>")
        reporte.write(f"<p>⏱️ Duración: {duracion:.2f} segundos</p>")
        reporte.write(f"<img src='{captura}' width='500'><br>")
    reporte.write("</div>")

# Tiempo total
fin_total = time.time()
duracion_total = fin_total - inicio_total
reporte.write(f"""
    <hr>
    <h2> Tiempo de Duración de la Prueba Automatizada <h2>
    <p><strong> ⏱️:</strong> {duracion_total:.2f} segundos</p>
</body>
</html>
""")

# Finalizar
driver.quit()
reporte.close()