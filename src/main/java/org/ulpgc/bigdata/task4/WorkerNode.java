package org.ulpgc.bigdata.task4;

import com.hazelcast.config.Config;
import com.hazelcast.core.Hazelcast;
import com.hazelcast.core.HazelcastInstance;

public class WorkerNode {
    public static void main(String[] args) {
        System.out.println("=== Iniciando NODO EXTRA (Worker) ===");
        
        // Configuración idéntica a la del Master
        Config config = new Config();
        config.setClusterName("matrix-cluster"); 
        
        // Arrancamos la instancia. 
        // Al estar en la misma red (localhost), se descubrirán automáticamente.
        HazelcastInstance hz = Hazelcast.newHazelcastInstance(config);
        
        System.out.println(">>> NODO WORKER LISTO Y ESPERANDO TAREAS <<<");
        System.out.println("No cierres esta ventana hasta terminar el benchmark.");
    }
}