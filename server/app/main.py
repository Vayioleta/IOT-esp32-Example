import csv # para almacenar los datos en un csv
from datetime import datetime, timedelta # para el manejo de fechas
from fastapi import FastAPI, HTTPException, Request # para crear el servidor api de recepcion de datos
app = FastAPI()

@app.get("/")
def read_root():
    return {
        "msg": "Esta es tu API en el puerto 8000."
    }

# Resivir datos del sensor
@app.post("/")
async def view_data(request: Request):
    try:
        # Obtener los datos dinámicos de la solicitud POST
        data = await request.json()
        print("Datos recibidos por POST:", data)

        with open('datos.csv', 'a', newline='') as file:
            # Crear un objeto escritor CSV
            csv_writer = csv.writer(file)

            # Escribir los datos en una nueva fila
            csv_writer.writerow([
                datetime.utcnow().isoformat(),
                data.get("temperatura"),
                data.get("humedad"),
                data.get("viento")
            ])
            
        return {"mensaje": "Datos recibidos y guardados correctamente en el archivo CSV"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Generar Grafico para la temperatura

import io
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.responses import StreamingResponse
import matplotlib.dates as mdates


# Función para leer los datos del archivo CSV y devolver un DataFrame de pandas
def read_csv_data():
    try:
        with open('datos.csv', 'r') as file:
            # Leer el contenido del archivo CSV en un DataFrame de pandas
            df = pd.read_csv(file, parse_dates=['timestamp'])
        return df
    except FileNotFoundError:
        return None


# Mostrar grafico de temperatura respecto al tiempo
@app.get("/grafica-temperatura/")
def plot_temperature_graph():
    # Leer los datos del archivo CSV
    df = read_csv_data()

    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No hay datos disponibles para generar la gráfica")

    # Filtrar solo los últimos 10 segundos
    last_10_seconds = datetime.now() - timedelta(seconds=20)
    df_last_seconds = df[df['timestamp'] > last_10_seconds]

    if df_last_seconds.empty:
        raise HTTPException(status_code=404, detail="No hay suficientes datos para mostrar los últimos 10 segundos")


    # Ajustar el tamaño de la figura para que sea más ancha
    plt.figure(figsize=(20, 6))

    # Crear la gráfica
    plt.plot(df_last_seconds['timestamp'], df_last_seconds['temperatura'], marker='o')
    plt.title('Gráfica de Temperatura en los últimos 20 segundos')
    plt.xlabel('Tiempo')
    plt.ylabel('Temperatura')

    # Configurar los ejes de tiempo para incluir segundos
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=1))  # Ajusta el intervalo según sea necesario
    
    # Separar un poco las etiquetas en el eje x para mejorar la legibilidad
    plt.xticks(rotation=45, ha='right', fontsize=12)

    plt.xticks(rotation=45)
    plt.tight_layout()

    # Convertir la gráfica a un formato de bytes
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    # Devolver la imagen generada como respuesta utilizando StreamingResponse
    return StreamingResponse(io.BytesIO(img_bytes.read()), media_type="image/png")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
