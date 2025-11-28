import pandas as pd
import matplotlib.pyplot as plt
import os

def pregunta_01():
    """
    Crea un dashboard estático en HTML con información de shipping-data.csv.
    """
    # Define la ruta al archivo de datos
    # Asumimos que la Opción 1 de la respuesta anterior es la correcta.
    data_file_path = os.path.join(os.path.dirname(__file__), "..", "files", "input", "shipping-data.csv")
    
    # Define la ruta de la carpeta de salida para los documentos
    docs_folder_path = os.path.join(os.path.dirname(__file__), "..", "docs")

    # Cargar los datos
    try:
        df = pd.read_csv(data_file_path)
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró en la ruta: {data_file_path}")
        print("Por favor, verifica la ubicación de 'shipping-data.csv' y descomenta la opción de ruta correcta.")
        return 

    # Crear la carpeta 'docs' si no existe
    os.makedirs(docs_folder_path, exist_ok=True)

    # Columnas a visualizar y sus nombres de archivo esperados por el test
    plot_configs = {
        'Warehouse_block': {'title': 'Distribución de Warehouse Block', 'filename': 'shipping_per_warehouse.png'},
        'Mode_of_Shipment': {'title': 'Distribución de Mode of Shipment', 'filename': 'mode_of_shipment.png'},
        'Customer_rating': {'title': 'Distribución de Customer Rating', 'filename': 'average_customer_rating.png'},
        'Weight_in_gms': {'title': 'Distribución de Weight in gms', 'filename': 'weight_distribution.png'}, 
    }

    image_files = {}

    # Generar gráficos individuales y guardarlos
    for col, config in plot_configs.items():
        plt.figure(figsize=(8, 6)) 

        if col in ['Warehouse_block', 'Mode_of_Shipment', 'Customer_rating']:
            df[col].value_counts().sort_index().plot(kind='bar')
            plt.title(config['title'])
            plt.xlabel(col)
            plt.ylabel('Frecuencia')
            plt.xticks(rotation=0) 
        elif col == 'Weight_in_gms':
            plt.hist(df[col], bins=20, edgecolor='black')
            plt.title(config['title'])
            plt.xlabel(col)
            plt.ylabel('Frecuencia')
        
        plt.tight_layout()

        image_path = os.path.join(docs_folder_path, config['filename'])
        plt.savefig(image_path)
        plt.close() 
        image_files[col] = config['filename'] 

    # Construir el HTML (asegurando que los nombres de archivo en el HTML coincidan con los guardados)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shipping Data Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; }}
            .dashboard-container {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }}
            .chart-card {{
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                padding: 15px;
                text-align: center;
                width: 45%; 
                box-sizing: border-box; 
            }}
            .chart-card img {{ max-width: 100%; height: auto; border-radius: 4px; }}
            h1 {{ text-align: center; color: #333; }}
        </style>
    </head>
    <body>
        <h1>Shipping Data Dashboard</h1>
        <div class="dashboard-container">
            <div class="chart-card">
                <h2>Warehouse Block Distribution</h2>
                <img src="{image_files['Warehouse_block']}" alt="Warehouse Block Distribution">
            </div>
            <div class="chart-card">
                <h2>Mode of Shipment Distribution</h2>
                <img src="{image_files['Mode_of_Shipment']}" alt="Mode of Shipment Distribution">
            </div>
            <div class="chart-card">
                <h2>Customer Rating Distribution</h2>
                <img src="{image_files['Customer_rating']}" alt="Customer Rating Distribution">
            </div>
            <div class="chart-card">
                <h2>Weight in Grams Distribution</h2>
                <img src="{image_files['Weight_in_gms']}" alt="Weight in Grams Distribution">
            </div>
        </div>
    </body>
    </html>
    """

    # Guarda el contenido HTML en un archivo
    # ¡CORRECCIÓN CLAVE AQUÍ! Cambiado de 'dashboard.html' a 'index.html'
    dashboard_file_path = os.path.join(docs_folder_path, 'index.html') 
    with open(dashboard_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Dashboard creado en: {dashboard_file_path}")