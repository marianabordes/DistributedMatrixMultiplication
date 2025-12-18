package org.ulpgc.bigdata.task4;

import java.util.stream.IntStream;

public class ParallelMatrixMultiplication implements MatrixMultiplier {

    @Override
    public double[][] multiply(double[][] A, double[][] B) {
        int rowsA = A.length;
        int colsA = A[0].length;
        int colsB = B[0].length;

        if (colsA != B.length) {
            throw new IllegalArgumentException("Dimensiones incompatibles.");
        }

        double[][] C = new double[rowsA][colsB];

        // Paralelizamos el bucle exterior (las filas de A)
        // Java se encarga de repartir estas filas entre los núcleos disponibles
        IntStream.range(0, rowsA).parallel().forEach(i -> {
            for (int j = 0; j < colsB; j++) {
                double sum = 0.0;
                for (int k = 0; k < colsA; k++) {
                    sum += A[i][k] * B[k][j];
                }
                C[i][j] = sum;
            }
        });

        return C;
    }

    @Override
    public String getName() {
        return "Parallel (Java Streams)";
    }
}