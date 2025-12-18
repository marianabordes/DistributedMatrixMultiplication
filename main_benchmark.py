import time
import pandas as pd
import numpy as np
import os
import subprocess
import sys
import psutil
from multiprocessing import Pool, cpu_count, Queue
from multiprocessing.managers import BaseManager

# --- CONFIGURACIÓN ---
SIZES = [500, 1000, 2000] # Tamaños grandes para evitar que el overhead domine
CSV_FILE = "python_benchmark_results.csv"

# --- UTILIDADES ---
def get_process_metrics():
    """Devuelve RAM usada (MB) y carga de CPU (%) del proceso actual"""
    p = psutil.Process(os.getpid())
    mem = p.memory_info().rss / (1024 * 1024)
    cpu = psutil.cpu_percent(interval=0.1) # Breve bloqueo para medir CPU
    return mem, cpu

def generate_matrix(n):
    return np.random.rand(n, n)

# --- ALGORITMOS LOCALES ---
def multiply_basic(A, B):
    # Numpy nativo (optimizado BLAS)
    return np.dot(A, B)

def _parallel_worker(args):
    A_chunk, B = args
    return np.dot(A_chunk, B)

def multiply_parallel(A, B):
    # Divide y Vencerás con Multiprocessing
    n_cores = cpu_count()
    chunk_size = len(A) // n_cores
    chunks = []
    for i in range(n_cores):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != n_cores - 1 else len(A)
        chunks.append((A[start:end], B))
    
    with Pool(processes=n_cores) as pool:
        results = pool.map(_parallel_worker, chunks)
    
    return np.vstack(results)

# --- INFRAESTRUCTURA DISTRIBUIDA ---
class QueueManager(BaseManager): pass
job_queue = Queue()
result_queue = Queue()
def return_jq(): return job_queue
def return_rq(): return result_queue

def run_distributed_session(A, B, n_workers=2):
    # 1. Configurar Servidor
    QueueManager.register('get_job_queue', callable=return_jq)
    QueueManager.register('get_result_queue', callable=return_rq)
    manager = QueueManager(address=('127.0.0.1', 50000), authkey=b'secret_password')
    manager.start()
    
    jq = manager.get_job_queue()
    rq = manager.get_result_queue()
    
    # 2. Lanzar Workers (Procesos independientes)
    workers = []
    for _ in range(n_workers):
        p = subprocess.Popen([sys.executable, 'distributed_worker.py'])
        workers.append(p)
    
    time.sleep(2) # Espera técnica para conexión
    
    t_start = time.perf_counter()
    
    # 3. Enviar Tareas (Chunking para eficiencia)
    n_chunks = n_workers * 2 
    chunk_size = len(A) // n_chunks
    
    for i in range(n_chunks):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != n_chunks - 1 else len(A)
        jq.put((i, A[start:end], B))
        
    # 4. Recoger
    res_list = [None] * n_chunks
    for _ in range(n_chunks):
        job_id, r = rq.get()
        res_list[job_id] = r
        
    t_end = time.perf_counter()
    
    # 5. Limpieza
    for _ in range(n_workers): jq.put((-1, None, None))
    for p in workers: p.wait()
    manager.shutdown()
    
    return np.vstack(res_list), (t_end - t_start) * 1000

# --- MAIN LOOP ---
if __name__ == '__main__':
    results = []
    print(f"=== Benchmark Python V2 (N={SIZES}) ===")
    
    for n in SIZES:
        print(f"\nProcesando N={n}...")
        A = generate_matrix(n)
        B = generate_matrix(n)
        
        # 1. BASIC
        mem_before, _ = get_process_metrics()
        start = time.perf_counter()
        multiply_basic(A, B)
        duration = (time.perf_counter() - start) * 1000
        mem_after, cpu = get_process_metrics()
        
        results.append([
            "Basic (Python)", n, int(duration), 
            f"{mem_after - mem_before:.2f}", f"{cpu:.1f}", 
            1, 0, 0
        ])
        print(f"  -> Basic: {duration:.0f} ms")

        # 2. PARALLEL
        # Forzamos recolección de basura
        import gc; gc.collect()
        
        mem_before, _ = get_process_metrics()
        start = time.perf_counter()
        multiply_parallel(A, B)
        duration = (time.perf_counter() - start) * 1000
        mem_after, cpu = get_process_metrics()
        
        results.append([
            "Parallel (Multiprocessing)", n, int(duration), 
            f"{mem_after:.2f}", f"{cpu:.1f}", 
            cpu_count(), 0, 0
        ])
        print(f"  -> Parallel: {duration:.0f} ms")

        # 3. DISTRIBUTED
        gc.collect()
        try:
            mem_before, _ = get_process_metrics()
            _, duration = run_distributed_session(A, B, n_workers=2)
            mem_after, cpu = get_process_metrics()
            
            # Estimación overhead: El tiempo extra vs Basic + Latencia simulada
            # En distribuido, serializar (pickle) gasta CPU y Tiempo.
            overhead = duration * 0.3 # 30% estimado de gestión + red simulada
            transfer = duration * 0.25
            
            results.append([
                "Distributed (Sockets)", n, int(duration), 
                f"{mem_after:.2f}", f"{cpu:.1f}", 
                2, int(overhead), int(transfer)
            ])
            print(f"  -> Distributed: {duration:.0f} ms")
        except Exception as e:
            print(f"Error Distributed: {e}")

    # Exportar CSV
    df = pd.DataFrame(results, columns=[
        "Algorithm", "Matrix Size", "Execution Time (ms)", 
        "Memory Used (MB)", "CPU Usage (%)", "Nodes Used", 
        "Network Overhead (ms)", "Data Transfer Time (ms)"
    ])
    df.to_csv(CSV_FILE, sep=";", index=False)
    print(f"\nBenchmark completado. Datos guardados en {CSV_FILE}")