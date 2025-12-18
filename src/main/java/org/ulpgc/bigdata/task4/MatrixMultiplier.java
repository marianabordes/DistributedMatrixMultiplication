package org.ulpgc.bigdata.task4;

public interface MatrixMultiplier {
    /**
     * Realiza la multiplicación de matrices C = A x B
     */
    double[][] multiply(double[][] A, double[][] B);

    /**
     * Devuelve el nombre del algoritmo para los logs/CSV
     */
    String getName();
}