import pandas as pd
import numpy as np
import math
import tkinter as tk
from tkinter import filedialog

# Abrir un cuadro de diálogo para seleccionar el archivo Excel
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal

ruta_excel = filedialog.askopenfilename(
    title="Selecciona el archivo Excel",
    filetypes=[("Archivos de Excel", "*.xlsx *.xls")]
)
if not ruta_excel:
    raise Exception("No se seleccionó ningún archivo.")


columna = 'A'                  # columna con los datos
hoja = 0                       # índice o nombre de la hoja
n_clases = 6                   # número de clases para agrupar

# === LECTURA DE DATOS ===
df = pd.read_excel(ruta_excel, usecols=columna, sheet_name=hoja)
df.dropna(inplace=True)  # elimina celdas vacías
datos = df.iloc[:, 0].values

# === PARÁMETROS BÁSICOS ===
min_valor = min(datos)
max_valor = max(datos)
rango = max_valor - min_valor
amplitud = math.ceil(rango / n_clases)

# === TABLA DE FRECUENCIAS ===
tabla = []

lim_inf = min_valor
for i in range(n_clases):
    lim_sup = lim_inf + amplitud
    clase = [lim_inf, lim_sup]
    marca = (lim_inf + lim_sup) / 2
    freq = sum((datos >= lim_inf) & (datos < lim_sup)) if i < n_clases - 1 else sum((datos >= lim_inf) & (datos <= lim_sup))
    tabla.append({'Clase': f'{lim_inf:.2f} - {lim_sup:.2f}',
                  'Marca': marca,
                  'Frecuencia': freq})
    lim_inf = lim_sup

# === FRECUENCIAS ADICIONALES ===
total = sum(row['Frecuencia'] for row in tabla)
fa = 0
fra = 0

for row in tabla:
    freq = row['Frecuencia']
    row['F. Acumulada'] = fa + freq
    row['F. Relativa'] = freq / total
    row['F.R. Acumulada'] = fra + freq / total
    fa += freq
    fra += freq / total

tabla_df = pd.DataFrame(tabla)

# === ESTADÍSTICAS ===
marcas = np.array([row['Marca'] for row in tabla])
frecuencias = np.array([row['Frecuencia'] for row in tabla])
media = np.average(marcas, weights=frecuencias)

# Mediana
acum = np.cumsum(frecuencias)
n = sum(frecuencias)
for i, fa in enumerate(acum):
    if fa >= n / 2:
        l = float(tabla[i]['Clase'].split(' - ')[0])
        f = tabla[i]['Frecuencia']
        F = acum[i - 1] if i > 0 else 0
        h = amplitud
        mediana = l + ((n/2 - F) / f) * h
        break

# Moda (por fórmula de moda para clases)
moda = None
for i in range(1, n_clases-1):
    f0 = tabla[i - 1]['Frecuencia']
    f1 = tabla[i]['Frecuencia']
    f2 = tabla[i + 1]['Frecuencia']
    if f1 > f0 and f1 > f2:
        l = float(tabla[i]['Clase'].split(' - ')[0])
        d1 = f1 - f0
        d2 = f1 - f2
        moda = l + (d1 / (d1 + d2)) * amplitud
        break

# Varianza y Desviación
varianza = np.average((marcas - media)**2, weights=frecuencias)
desviacion = np.sqrt(varianza)

# Cuartiles
cuartiles = []
for k in [0.25, 0.5, 0.75]:
    for i, fa in enumerate(acum):
        if fa >= k * n:
            l = float(tabla[i]['Clase'].split(' - ')[0])
            f = tabla[i]['Frecuencia']
            F = acum[i - 1] if i > 0 else 0
            h = amplitud
            Q = l + ((k * n - F) / f) * h
            cuartiles.append(Q)
            break

# === RESULTADOS ===
print("\n=== TABLA DE FRECUENCIAS AGRUPADAS ===\n")
print(tabla_df)

print("\n=== MEDIDAS ESTADÍSTICAS ===")
print(f"Media: {media:.2f}")
print(f"Mediana: {mediana:.2f}")
print(f"Moda: {moda:.2f}" if moda else "Moda: No definida")
print(f"Varianza: {varianza:.2f}")
print(f"Desviación estándar: {desviacion:.2f}")
print(f"Cuartiles: Q1={cuartiles[0]:.2f}, Q2={cuartiles[1]:.2f}, Q3={cuartiles[2]:.2f}")
