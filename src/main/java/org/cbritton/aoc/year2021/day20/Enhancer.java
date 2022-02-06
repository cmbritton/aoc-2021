package org.cbritton.aoc.year2021.day20;

public class Enhancer {

    static final int KERNEL_SIZE = 3;
    static final int LEFT_KERNEL_BOUNDARY = -(KERNEL_SIZE / 2);
    static final int RIGHT_KERNEL_BOUNDARY = LEFT_KERNEL_BOUNDARY + (KERNEL_SIZE - 1);
    static final int LOWER_KERNEL_BOUNDARY = -(KERNEL_SIZE / 2);
    static final int UPPER_KERNEL_BOUNDARY = LOWER_KERNEL_BOUNDARY + (KERNEL_SIZE - 1);

    int[] algorithm = null;

    public Enhancer(int[] algorithm) {
        this.algorithm = algorithm;
    }

    Image enhance(Image image) {

        Image enhancedImage = new Image();
        enhancedImage.isExtendedPixelsLit = !image.isExtendedPixelsLit;

        for (int x = image.minX - 1; x <= image.maxX + 1; ++x) {
            for (int y = image.minY - 1; y <= image.maxY + 1; ++y) {
                enhancePixel(x, y, image, enhancedImage);
            }
        }
        return enhancedImage;
    }

    private void enhancePixel(int x, int y, Image image, Image enhancedImage) {

        if (1 == this.algorithm[getEnhancementIndex(x, y, image)]) {
            enhancedImage.add(new Point(x, y));
        }
        return;
    }

    private int getEnhancementIndex(int x, int y, Image image) {

        Point point = new Point();
        int enhancementIndex = 0;
        for (int i = LEFT_KERNEL_BOUNDARY; i <= RIGHT_KERNEL_BOUNDARY; ++i) {
            for (int j = LOWER_KERNEL_BOUNDARY; j <= UPPER_KERNEL_BOUNDARY; ++j) {
                point.x = x + i;
                point.y = y + j;
                enhancementIndex <<= 1;
                if (image.isPixelLit(point)) {
                    enhancementIndex |= 1;
                }
            }
        }
        return enhancementIndex;
    }
}
