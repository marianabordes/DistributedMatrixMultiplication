package org.ulpgc.bigdata.task4;

public class BasicMatrixMultiplication implements MatrixMultiplier {

    @Override
    public double[][] multiply(double[][] A, double[][] B) {
        int rowsA = A.length;
        int colsA = A[0].length;
        int colsB = B[0].length;

        if (colsA != B.length) {
            throw new IllegalArgumentException("Dimensiones incompatibles para multiplicación.");
        }

        double[][] C = new double[rowsA][colsB];

        // Algoritmo clásico secuencial (Triple bucle)
        for (int i = 0; i < rowsA; i++) {
            for (int j = 0; j < colsB; j++) {
                double sum = 0.0;
                for (int k = 0; k < colsA; k++) {
                    sum += A[i][k] * B[k][j];
                }
                C[i][j] = sum;
            }
        }
        return C;
    }

    @Override
    public String getName() {
        return "Basic (Sequential)";
    }
}