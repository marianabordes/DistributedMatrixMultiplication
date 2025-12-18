import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# --- CONFIGURACIÓN ESTÉTICA (Estilo Académico) ---
sns.set_style("whitegrid")
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,  # Alta resolución para el PDF
    'lines.linewidth': 2.5,
    'lines.markersize': 8
})

OUTPUT_DIR = "plots"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def load_data():
    # Cargar Java
    try:
        df_java = pd.read_csv('benchmark_results.csv', sep=';')
        df_java['Language'] = 'Java'
    except:
        print("⚠ No se encontró benchmark_results.csv. Usando datos dummy para Java.")
        df_java = pd.DataFrame()

    # Cargar Python
    try:
        df_py = pd.read_csv('python_benchmark_results.csv', sep=';')
        df_py['Language'] = 'Python'
    except:
        print("⚠ No se encontró python_benchmark_results.csv.")
        df_py = pd.DataFrame()

    return df_java, df_py

# --- 1. TIEMPO DE EJECUCIÓN (Log Scale) ---
def plot_execution_time(df, lang):
    if df.empty: return
    plt.figure(figsize=(10, 6))
    
    # Filtrar algoritmos relevantes
    ax = sns.lineplot(data=df, x='Matrix Size', y='Execution Time (ms)', 
                      hue='Algorithm', style='Algorithm', markers=True, dashes=False)
    
    plt.yscale('log')  # Escala logarítmica es vital aquí por la diferencia masiva
    plt.title(f'Execution Time vs Matrix Size ({lang}) - Log Scale')
    plt.ylabel('Time (ms) [Log Scale]')
    plt.xlabel('Matrix Size (N)')
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    
    filename = f"{OUTPUT_DIR}/1_ExecutionTime_{lang}.png"
    plt.savefig(filename, bbox_inches='tight')
    print(f"Generado: {filename}")
    plt.close()

# --- 2. ANÁLISIS DE OVERHEAD DE RED (Vital para Tarea 4) ---
def plot_network_overhead(df, lang):
    if df.empty: return
    
    # Solo el algoritmo distribuido
    dist_df = df[df['Algorithm'].str.contains('Distributed')].copy()
    
    if dist_df.empty: return

    plt.figure(figsize=(10, 6))
    
    # Preparar datos para Stacked Bar
    # Total Height = Execution Time
    # Bottom = Processing Time (Execution - Overhead)
    # Top = Overhead
    
    bar_width = 0.5
    indices = np.arange(len(dist_df))
    
    processing_time = dist_df['Execution Time (ms)'] - dist_df['Network Overhead (ms)']
    overhead = dist_df['Network Overhead (ms)']
    
    p1 = plt.bar(indices, processing_time, width=bar_width, label='Processing Time', color='#4a90e2')
    p2 = plt.bar(indices, overhead, width=bar_width, bottom=processing_time, label='Network/Serialization Overhead', color='#e74c3c')
    
    plt.title(f'Impact of Network Overhead in Distributed {lang}')
    plt.xlabel('Matrix Size (N)')
    plt.ylabel('Time (ms)')
    plt.xticks(indices, dist_df['Matrix Size'])
    plt.legend()
    
    # Añadir porcentajes
    for i, (p_val, o_val, total) in enumerate(zip(processing_time, overhead, dist_df['Execution Time (ms)'])):
        pct = (o_val / total) * 100
        if pct > 5: # Solo mostrar si es relevante
            plt.text(i, total + (total*0.02), f"{pct:.1f}% Overhead", ha='center', fontsize=9, fontweight='bold')

    filename = f"{OUTPUT_DIR}/2_NetworkOverhead_{lang}.png"
    plt.savefig(filename, bbox_inches='tight')
    print(f"Generado: {filename}")
    plt.close()

# --- 3. MEMORY EXPLOSION (Distributed vs Local) ---
def plot_memory_comparison(df, lang):
    if df.empty: return
    plt.figure(figsize=(10, 6))
    
    sns.lineplot(data=df, x='Matrix Size', y='Memory Used (MB)', 
                 hue='Algorithm', style='Algorithm', markers=True)
    
    plt.title(f'Memory Usage vs Matrix Size ({lang})')
    plt.ylabel('Memory (MB)')
    plt.xlabel('Matrix Size (N)')
    
    filename = f"{OUTPUT_DIR}/3_MemoryUsage_{lang}.png"
    plt.savefig(filename, bbox_inches='tight')
    print(f"Generado: {filename}")
    plt.close()

# --- 4. COMPARATIVA JAVA vs PYTHON (Distributed Only) ---
def plot_lang_comparison(df_java, df_py):
    if df_java.empty or df_py.empty: return
    
    # Filtrar solo Distributed
    d_java = df_java[df_java['Algorithm'].str.contains('Distributed')][['Matrix Size', 'Execution Time (ms)']].copy()
    d_java['Implementation'] = 'Java (Hazelcast)'
    
    d_py = df_py[df_py['Algorithm'].str.contains('Distributed')][['Matrix Size', 'Execution Time (ms)']].copy()
    d_py['Implementation'] = 'Python (Sockets)'
    
    combined = pd.concat([d_java, d_py])
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=combined, x='Matrix Size', y='Execution Time (ms)', hue='Implementation', palette='viridis')
    
    plt.title('Performance Comparison: Java vs Python (Distributed)')
    plt.ylabel('Execution Time (ms)')
    plt.xlabel('Matrix Size (N)')
    
    filename = f"{OUTPUT_DIR}/4_JavaVsPython_Distributed.png"
    plt.savefig(filename, bbox_inches='tight')
    print(f"Generado: {filename}")
    plt.close()

# --- MAIN ---
if __name__ == "__main__":
    df_java, df_py = load_data()
    
    print("--- Generando Gráficos ---")
    
    # Gráficos Java
    if not df_java.empty:
        plot_execution_time(df_java, 'Java')
        plot_network_overhead(df_java, 'Java')
        plot_memory_comparison(df_java, 'Java')
        
    # Gráficos Python
    if not df_py.empty:
        plot_execution_time(df_py, 'Python')
        plot_network_overhead(df_py, 'Python')
    
    # Comparativa
    plot_lang_comparison(df_java, df_py)
    
    print("\n¡Listo! Revisa la carpeta 'plots/'")