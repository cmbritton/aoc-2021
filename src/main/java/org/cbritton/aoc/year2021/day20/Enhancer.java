package org.cbritton.aoc.year2021.day20;

import java.util.Arrays;

public class Enhancer {

    static final int PAD = 2;

    int[] algorithm = null;

    boolean firstTime = true;

    public Enhancer(int[] algorithm) {
        this.algorithm = algorithm;
    }

    int[][] pad(int[][] imageData) {

        int[][] paddedImageData = new int[imageData.length + (PAD * 2)][imageData[0].length + (PAD * 2)];
        for (int i = 0; i < paddedImageData.length; ++i) {
            Arrays.fill(paddedImageData[i], 0);
            if ((i >= PAD) && (i < (paddedImageData.length - PAD))) {
                System.arraycopy(imageData[i - PAD], 0, paddedImageData[i], PAD, imageData[i - PAD].length);
            }
        }
        return paddedImageData;
    }

    void extendRight(int[][] imageData) {

        for (int i = 0; i < imageData.length; ++i) {
            for (int j = 0; j < PAD; ++j) {
                imageData[i][imageData.length - j - 1] = imageData[i][imageData.length - PAD - 1];
            }
        }
        return;
    }

    void extendLeft(int[][] imageData) {

        for (int i = 0; i < imageData.length; ++i) {
            for (int j = 0; j < PAD; ++j) {
                imageData[i][j] = imageData[i][PAD];
            }
        }
        return;
    }

    int[][] extend(int[][] imageData) {

        int[][] extendedImageData = new int[imageData.length + (PAD * 2)][imageData[0].length + (PAD * 2)];
        for (int i = 0; i < extendedImageData.length; ++i) {
            Arrays.fill(extendedImageData[i], 0);
            if (i < PAD) {
                System.arraycopy(imageData[0], 0, extendedImageData[i], PAD, imageData[0].length);
            } else if (i >= extendedImageData.length - PAD) {
                System.arraycopy(imageData[imageData.length - 1], 0, extendedImageData[i], PAD,
                        imageData[imageData.length - 1].length);
            } else {
                System.arraycopy(imageData[i - PAD], 0, extendedImageData[i], PAD, imageData[i - PAD].length);
            }
        }
        extendLeft(extendedImageData);
        extendRight(extendedImageData);
        return extendedImageData;
    }

    Image enhance(Image image) {

        int[][] imageData = image.data;
//        if (firstTime) {
            imageData = pad(image.data);
//            firstTime = false;
//        } else {
//            imageData = extend(image.data);
//        }
        int rows = imageData.length;
        int cols = imageData[0].length;
        int[][] enhancedImageData = new int[rows][cols];
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                enhancePixel(i, j, imageData, enhancedImageData);
            }
        }
        return new Image(enhancedImageData);
    }

    private void enhancePixel(int row, int col, int[][]imageData, int[][]enhancedImageData) {
        enhancedImageData[row][col] = this.algorithm[getEnhancementIndex(row, col, imageData)];
    }

    private int getEnhancementIndex(int row, int col, int[][] imageData) {

        int enhancementIndex = 0;
        for (int i = -1; i < 2; ++i) {
            for (int j = -1; j < 2; ++j) {
                int subRow = row + i;
                int subCol = col + j;
                int pixelValue = getPixelValue(subRow, subCol, imageData);
                enhancementIndex |= (pixelValue << 8 - (((i + 1) * 3) + (j + 1)));
//                System.err.print(" " + pixelValue);
            }
//            System.err.println();
        }
//        System.err.println(", row=" + row + ", col=" + col + ", index=" + enhancementIndex);
        return enhancementIndex;
    }

    private int getPixelValue(int subRow, int subCol, int[][] imageData) {

        if ((subRow < 0) || (subRow > imageData.length - 1)) {
            return 0;
        } else if ((subCol < 0) || (subCol > imageData[0].length - 1)) {
            return 0;
        } else {
            return imageData[subRow][subCol];
        }
    }
}
