import numpy as np
import time
from multiprocessing import Pool, cpu_count

def generate_matrix(n):
    return np.random.rand(n, n)

# --- 1. Basic (Sequential) ---
def multiply_basic(A, B):
    return np.dot(A, B)

# --- 2. Parallel (Multiprocessing) ---
# Dividimos A en trozos y cada proceso multiplica su trozo por B
def _worker_multiply(args):
    row_A_chunk, B = args
    return np.dot(row_A_chunk, B)

def multiply_parallel(A, B):
    n_cores = cpu_count()
    # Dividir A en trozos (chunks) según cores
    chunk_size = len(A) // n_cores
    chunks = []
    for i in range(n_cores):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != n_cores - 1 else len(A)
        chunks.append((A[start:end], B))
    
    with Pool(processes=n_cores) as pool:
        results = pool.map(_worker_multiply, chunks)
    
    return np.vstack(results)