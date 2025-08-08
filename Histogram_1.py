import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# === Datos de la Tabla 3 ===
data = {
    "Variable evaluada": [
        "Factores internos",
        "Factores sociales",
        "Factores académicos",
        "Facultad donde estudias",
        "Carrera que estudias",
        "Semestre",
        "Género",
        "Edad",
        "Estado Civil",
        "Número de hijos en caso de tener",
        "Trabaja"
    ],
    "Factores internos": [1, 0.043, 0.355, 0.787, 0.873, 0.042, 0.076, 0.051, 0.012, 0.054, 0.839],
    "Factores sociales": [0.043, 1, 0.613, 0.004, 0.020, 0.003, 0.617, 0.033, 0.060, 0.040, 0.739],
    "Factores académicos": [0.355, 0.613, 1, 0.805, 0.782, 0.019, 0.632, 0.526, 0.070, 0.029, 0.716]
}

# Crear DataFrame
df = pd.DataFrame(data).set_index("Variable evaluada")

# Crear grafo vacío
G = nx.Graph()

# Agregar nodos
for var in df.index:
    G.add_node(var)

# Agregar aristas para correlaciones con |valor| > 0.5 y que no sean 1
for col in df.columns:
    for idx in df.index:
        val = df.loc[idx, col]
        if idx != col and abs(val) > 0.5 and abs(val) < 1:
            G.add_edge(idx, col, weight=abs(val), color='blue' if val > 0 else 'red')

# Obtener colores y pesos
edges = G.edges(data=True)
colors = [edata['color'] for _, _, edata in edges]
weights = [edata['weight'] * 5 for _, _, edata in edges]  # Multiplico para resaltar grosor

# Dibujar grafo
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, k=0.5, seed=42)  # Layout de red
nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')
nx.draw_networkx_edges(G, pos, edge_color=colors, width=weights)
plt.title("Tabla 3 - Network Graph de Correlaciones (> 0.5)", fontsize=14)
plt.axis('off')
plt.tight_layout()

# Guardar imagen
plt.savefig("tabla3_network_graph.png", dpi=300)
plt.show()

print("Gráfico guardado como: tabla3_network_graph.png")
