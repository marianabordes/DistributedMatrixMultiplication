import time
import numpy as np
from multiprocessing.managers import BaseManager
import os

class QueueManager(BaseManager): pass

def run_worker():
    # Registrar colas (misma firma que el Master)
    QueueManager.register('get_job_queue')
    QueueManager.register('get_result_queue')

    print(f"[Worker {os.getpid()}] Conectando al Master...")
    
    # Conexión local simulada
    m = QueueManager(address=('127.0.0.1', 50000), authkey=b'secret_password')
    try:
        m.connect()
    except:
        print("ERROR: No se encuentra el Master.")
        return

    job_queue = m.get_job_queue()
    result_queue = m.get_result_queue()
    
    print(f"[Worker {os.getpid()}] Listo y esperando.")
    
    while True:
        try:
            job = job_queue.get(timeout=5)
            job_id, row_A_chunk, B = job
            
            if job_id == -1: # Señal de parada
                break
            
            # 1. Simular Latencia de Red (Network Overhead)
            # En un cluster real, enviar B tarda tiempo. Aquí lo simulamos.
            # 0.5ms por cada 1MB de datos aprox.
            data_size_mb = (B.nbytes + row_A_chunk.nbytes) / (1024*1024)
            network_latency = data_size_mb * 0.05 
            time.sleep(network_latency)
            
            # 2. Cálculo Real
            res = np.dot(row_A_chunk, B)
            
            # Enviar resultado
            result_queue.put((job_id, res))
            
        except Exception:
            break
            
    print(f"[Worker {os.getpid()}] Cerrando.")

if __name__ == '__main__':
    run_worker()