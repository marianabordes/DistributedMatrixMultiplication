package org.ulpgc.bigdata.task4;

import com.hazelcast.core.Hazelcast;
import com.hazelcast.core.HazelcastInstance;
import com.hazelcast.core.IExecutorService;
import com.hazelcast.config.Config;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Future;

public class DistributedMatrixMultiplication implements MatrixMultiplier {

    private HazelcastInstance hazelcastInstance;

    public DistributedMatrixMultiplication() {
        // Configuración básica para evitar ruido en la consola
        Config config = new Config();
        config.setClusterName("matrix-cluster");
        // Iniciamos el nodo Hazelcast local (actúa como Master y Worker a la vez si está solo)
        this.hazelcastInstance = Hazelcast.newHazelcastInstance(config);
    }

    @Override
    public double[][] multiply(double[][] A, double[][] B) {
        int rowsA = A.length;
        int colsB = B[0].length;

        // Obtenemos el servicio de ejecución distribuida de Hazelcast
        IExecutorService executorService = hazelcastInstance.getExecutorService("matrix-executor");
        List<Future<double[]>> futures = new ArrayList<>();

        // 1. DISPATCH: Enviar tareas a la red
        // Por cada fila de A, creamos una tarea y la mandamos al clúster
        for (int i = 0; i < rowsA; i++) {
            MatrixMultiplicationTask task = new MatrixMultiplicationTask(A[i], B);
            futures.add(executorService.submit(task));
        }

        double[][] C = new double[rowsA][colsB];

        // 2. COLLECT: Recoger resultados
        // Esperamos a que los workers terminen y reconstruimos la matriz C
        for (int i = 0; i < rowsA; i++) {
            try {
                // future.get() bloquea hasta que el nodo remoto responde
                C[i] = futures.get(i).get(); 
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        return C;
    }

    // Método para apagar Hazelcast 
    public void shutdown() {
        hazelcastInstance.shutdown();
    }

    @Override
    public String getName() {
        return "Distributed (Hazelcast)";
    }

    public HazelcastInstance getHazelcastInstance() {
        return this.hazelcastInstance;
    }
}