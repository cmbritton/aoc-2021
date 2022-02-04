package org.cbritton.aoc.year2021.day20;

public class Image {

    int[][] data = null;

    public Image(int[][] data) {
        this.data = data;
    }

    int getLitPixelCount() {

        int litPixelCount = 0;
        for (int i = 0; i < data.length; ++i) {
            for (int j = 0; j < data[0].length; ++j) {
                if (data[i][j] == 1) {
                    litPixelCount++;
                }
            }
        }
        return litPixelCount;

    }

    void printImage() {

        for (int i = 0; i < data.length; ++i) {
            for (int j = 0; j < data[0].length; ++j) {
                if (data[i][j] == 0) {
                    System.out.print(".");
                } else {
                    System.out.print("#");
                }
            }
            System.out.println();
        }
        return;
    }
}
