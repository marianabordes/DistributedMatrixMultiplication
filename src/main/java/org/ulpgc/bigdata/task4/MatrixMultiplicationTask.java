package org.ulpgc.bigdata.task4;

import java.io.Serializable;
import java.util.concurrent.Callable;

public class MatrixMultiplicationTask implements Callable<double[]>, Serializable {
    
    private final double[] rowA;
    private final double[][] matrixB;

    public MatrixMultiplicationTask(double[] rowA, double[][] matrixB) {
        this.rowA = rowA;
        this.matrixB = matrixB;
    }

    @Override
    public double[] call() {
        // Esta lógica se ejecuta dentro del nodo Worker
        int colsB = matrixB[0].length;
        int commonDim = matrixB.length; // Filas de B (o columnas de A)
        
        double[] resultRow = new double[colsB];

        // Multiplicación de vector (fila A) x matriz (B)
        for (int j = 0; j < colsB; j++) {
            double sum = 0.0;
            for (int k = 0; k < commonDim; k++) {
                sum += rowA[k] * matrixB[k][j];
            }
            resultRow[j] = sum;
        }
        return resultRow;
    }
}