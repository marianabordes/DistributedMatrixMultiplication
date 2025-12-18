package org.ulpgc.bigdata.task4;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class CSVWriterUtility {
    private String filePath;

    public CSVWriterUtility(String filePath) {
        this.filePath = filePath;
    }

    // Escribe la cabecera del CSV
    public void writeHeader(String header) {
        try (PrintWriter writer = new PrintWriter(new FileWriter(filePath))) {
            writer.println(header);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Añade una línea de datos (append = true)
    public void writeRecord(String record) {
        try (PrintWriter writer = new PrintWriter(new FileWriter(filePath, true))) {
            writer.println(record);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}